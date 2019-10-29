#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    pyan.py - Generate approximate call graphs for Python programs.

    This program takes one or more Python source files, does a superficial
    analysis, and constructs a directed graph of the objects in the combined
    source, and how they define or use each other.  The graph can be output
    for rendering by e.g. GraphViz or yEd.
"""

import sys
import ast
import symtable
from glob import glob
from optparse import OptionParser  # TODO: migrate to argparse
import os.path
import re
#import math

# TODO: split to modules (at least the color stuff)
# TODO: add Cython support (strip type annotations in a preprocess step, then treat as Python)
# TODO: built-in functions (range(), enumerate(), zip(), iter(), ...):
#       add to a special scope "built-in" in analyze_scopes() (or ignore altogether)
# TODO: support Node-ifying ListComp et al, List, Tuple
# TODO: make the analyzer smarter (see individual TODOs)

class MsgLevel:
    ERROR   = 0
    WARNING = 1
    INFO    = 2
    DEBUG   = 3

verbosity = MsgLevel.WARNING
def message(msg, level):
    if level <= verbosity:
        print(msg, file=sys.stderr)

def format_alias(x):
    """Return human-readable description of an ast.alias (used in Import and ImportFrom nodes)."""
    if not isinstance(x, ast.alias):
        raise TypeError("Can only format an ast.alias; got %s" % type(x))

    if x.asname is not None:
        return "%s as %s" % (x.name, x.asname)
    else:
        return "%s" % (x.name)

def getname(x):
    """Return human-readable name of ast.Attribute or ast.Name. Pass through anything else."""
    if isinstance(x, ast.Attribute):
        return "%s.%s" % (getname(x.value), x.attr)  # x.value might also be an ast.Attribute (think "x.y.z")
    elif isinstance(x, ast.Name):
        return x.id
    else:
        return x

# Helper for handling binding forms.
def sanitize(exprs):
    """Convert ast.Tuples in exprs to Python tuples; wrap result in a Python tuple."""
    def process(expr):
        if isinstance(expr, (ast.Tuple, ast.List)):
            return expr.elts  # .elts is a Python tuple
        else:
            return [expr]
    if isinstance(exprs, (tuple, list)):
        return [process(expr) for expr in exprs]
    else:
        return process(exprs)

def get_module_name(filename):
    """Try to determine the full module name of a source file, by figuring out
    if its directory looks like a package (i.e. has an __init__.py file)."""

    if os.path.basename(filename) == '__init__.py':
        return get_module_name(os.path.dirname(filename))

    init_path = os.path.join(os.path.dirname(filename), '__init__.py')
    mod_name = os.path.basename(filename).replace('.py', '')

    if not os.path.exists(init_path):
        return mod_name

    return get_module_name(os.path.dirname(filename)) + '.' + mod_name

def hsl2rgb(H,S,L):
    import colorsys
    return colorsys.hls_to_rgb(H,L,S)

#def hsl2rgb(H,S,L):
#    """Convert HSL color tuple to RGB.
#
#    Parameters:  H,S,L, where
#        H,S,L = HSL values as double-precision floats, with each component in [0,1].
#
#    Return value:
#        R,G,B tuple
#
#    For more information:
#        https://en.wikipedia.org/wiki/HSL_and_HSV#From_HSL
#
#    """
#    if H < 0.0  or  H > 1.0:
#        raise ValueError("H component = %g out of range [0,1]" % H)
#    if S < 0.0  or  S > 1.0:
#        raise ValueError("S component = %g out of range [0,1]" % S)
#    if L < 0.0  or  L > 1.0:
#        raise ValueError("L component = %g out of range [0,1]" % L)
#
#    # hue chunk
#    Hpf = H / (60./360.) # "H prime, float" (H', float)
#    Hp = int(Hpf)  # "H prime" (H', int)
#    if Hp >= 6:  # catch special case 360deg = 0deg
#        Hp = 0
#
#    C = (1.0 - math.fabs(2.0*L - 1.0))*S  # HSL chroma
#    X = C * (1.0 - math.fabs( math.modf(Hpf / 2.0)[0] - 1.0 ))
#
#    if S == 0.0:  # H undefined if S == 0
#        R1,G1,B1 = (0.0, 0.0, 0.0)
#    elif Hp == 0:
#        R1,G1,B1 = (C,   X,   0.0)
#    elif Hp == 1:
#        R1,G1,B1 = (X,   C,   0.0)
#    elif Hp == 2:
#        R1,G1,B1 = (0.0, C,   X  )
#    elif Hp == 3:
#        R1,G1,B1 = (0.0, X,   C  )
#    elif Hp == 4:
#        R1,G1,B1 = (X,   0.0, C  )
#    elif Hp == 5:
#        R1,G1,B1 = (C,   0.0, X  )
#
#    # match the HSL Lightness
#    #
#    m = L - 0.5*C
#    R,G,B = (R1 + m, G1 + m, B1 + m)
#
#    return R,G,B

def htmlize_rgb(R,G,B,A=None):
    """HTML-ize an RGB(A) color.

    Parameters:  R,G,B[,alpha], where
        R,G,B = RGB values as double-precision floats, with each component in [0,1].
        alpha = optional alpha component for translucency, in [0,1]. (1.0 = opaque)

    Example:
        htmlize_rgb(1.0, 0.5, 0)       =>  "#FF8000"    (RGB)
        htmlize_rgb(1.0, 0.5, 0, 0.5)  =>  "#FF800080"  (RGBA)

    """
    if R < 0.0  or  R > 1.0:
        raise ValueError("R component = %g out of range [0,1]" % R)
    if G < 0.0  or  G > 1.0:
        raise ValueError("G component = %g out of range [0,1]" % G)
    if B < 0.0  or  B > 1.0:
        raise ValueError("B component = %g out of range [0,1]" % B)

    R = int(255.0*R)
    G = int(255.0*G)
    B = int(255.0*B)

    if A is not None:
        if A < 0.0  or  A > 1.0:
            raise ValueError("alpha component = %g out of range [0,1]" % A)
        A = int(255.0*A)
        return "#%02X%02X%02X%02X" % (R, G, B, A)
    else:
        return "#%02X%02X%02X" % (R, G, B)


# This class mainly stores auxiliary information about AST nodes, for the
# purposes of generating the call graph.
#
# Namespaces also get a Node (with no associated AST node).
#
# Note the use of the term "node" for two different concepts:
#  - this Node class
#  - AST nodes (the "node" argument of CallGraphVisitor.visit_*())
#
class Node:
    """A node is an object in the call graph.  Nodes have names, and are in
    namespaces.  The full name of a node is its namespace, a dot, and its name.
    If the namespace is None, it is rendered as *, and considered as an unknown
    node.  The meaning of this is that a use-edge to an unknown node is created
    when the analysis cannot determine which actual node is being used."""

    def __init__(self, namespace, name, ast_node):
        self.namespace = namespace
        self.name = name
        self.defined = namespace is None  # assume that unknown nodes are defined
        self.ast_node = ast_node

    def get_short_name(self):
        """Return the short name (i.e. excluding the namespace), of this Node.
        Names of unknown nodes will include the *. prefix."""

        if self.namespace is None:
            return '*.' + self.name
        else:
            return self.name

    def get_annotated_name(self):
        """Return the short name, plus module and line number of definition site, if available.
        Names of unknown nodes will include the *. prefix."""
        if self.namespace is None:
            return '*.' + self.name
        else:
            if self.get_level() >= 1 and self.ast_node is not None:
                return "%s\\n(%s.py:%d)" % (self.name, self.namespace.split('.',1)[0], self.ast_node.lineno)
            else:
                return self.name

    def get_name(self):
        """Return the full name of this node."""

        if self.namespace == '':
            return self.name
        elif self.namespace is None:
            return '*.' + self.name
        else:
            return self.namespace + '.' + self.name

    def get_level(self):
        """Return the level of this node (in terms of nested namespaces).

        The level is defined as the number of '.' in the namespace, plus one.
        Top level is level 0.

        """
        if self.namespace == "":
            return 0
        else:
            return 1 + self.namespace.count('.')

    def get_toplevel_namespace(self):
        """Return the name of the top-level namespace of this node, or "" if none."""
        if self.namespace == "":
            return ""
        if self.namespace is None:  # group all unknowns in one namespace, "*"
            return "*"

        idx = self.namespace.find('.')
        if idx > -1:
            return self.namespace[0:idx]
        else:
            return self.namespace

    def get_label(self):
        """Return a label for this node, suitable for use in graph formats.
        Unique nodes should have unique labels; and labels should not contain
        problematic characters like dots or asterisks."""

        return self.get_name().replace('.', '__').replace('*', '')

    def __repr__(self):
        return '<Node %s>' % self.get_name()


# Adaptor that makes scopes look somewhat like those from the Python 2 compiler module
# (as far as our CallGraphVisitor is concerned)
#
class Scope:
    def __init__(self, table):
        name = table.get_name()
        if name == 'top':
            name = ''  # Pyan defines the top level as anonymous
        self.name = name
        self.type = table.get_type()  # useful for __repr__()
        self.defs = {iden:None for iden in table.get_identifiers()}  # name:assigned_value

    def __repr__(self):
        return "<Scope: %s %s>" % (self.type, self.name)

# The visitor has been converted by comparing these tables in Python docs:
#
# https://docs.python.org/2/library/compiler.html#module-compiler.ast
# https://docs.python.org/3/library/ast.html#abstract-grammar
#
class CallGraphVisitor(ast.NodeVisitor):
    """A visitor that can be walked over a Python AST, and will derive
    information about the objects in the AST and how they use each other.

    A single CallGraphVisitor object can be run over several ASTs (from a
    set of source files).  The resulting information is the aggregate from
    all files.  This way use information between objects in different files
    can be gathered."""

    def __init__(self, filenames):
        # full module names for all given files
        self.module_names = {}
        for filename in filenames:
            mod_name = get_module_name(filename)
            short_name = mod_name.rsplit('.', 1)[-1]
            self.module_names[short_name] = mod_name
        self.filenames = filenames

        # data gathered from analysis
        self.defines_edges = {}
        self.uses_edges = {}
        self.nodes = {}   # Node name: list of Node objects (in possibly different namespaces)
        self.scopes = {}  # fully qualified name of namespace: Scope object
        self.ast_node_to_namespace = {}  # AST node: fully qualified name of namespace

        # current context for analysis
        self.module_name = None
        self.name_stack  = []  # for building namespace name, node naming
        self.scope_stack = []  # the Scope objects
        self.class_stack = []  # for resolving "self"
        self.last_value  = None

    def process(self, filename):
        """Analyze the specified Python source file."""

        if filename not in self.filenames:
            raise ValueError("Filename '%s' has not been preprocessed (was not given to __init__, which got %s)" % (filename, self.filenames))
        with open(filename, "rt", encoding="utf-8") as f:
            content = f.read()
        self.module_name = get_module_name(filename)
        self.analyze_scopes(content, filename)
        self.visit(ast.parse(content, filename))
        self.module_name = None

    def postprocess(self):
        """Finalize the analysis by postprocessing the results."""

        self.contract_nonexistents()
        self.expand_unknowns()
        self.cull_inherited()

    def visit_Module(self, node):
        message("Module", level=MsgLevel.DEBUG)

        ns = self.module_name
        self.name_stack.append(ns)
        self.scope_stack.append(self.scopes[ns])
        self.ast_node_to_namespace[node] = ns  # must be added manually since we don't self.get_node() here
        self.generic_visit(node)  # visit the **children** of node
        self.scope_stack.pop()
        self.name_stack.pop()
        self.last_value = None

    def visit_ClassDef(self, node):
        message("ClassDef %s" % (node.name), level=MsgLevel.DEBUG)

        from_node = self.get_current_namespace()
        ns = from_node.get_name()
        to_node = self.get_node(ns, node.name, node)
        if self.add_defines_edge(from_node, to_node):
            message("Def from %s to Class %s" % (from_node, to_node), level=MsgLevel.INFO)

        self.set_value(node.name, to_node)

        self.class_stack.append(to_node)
        self.name_stack.append(node.name)
        inner_ns = self.get_current_namespace().get_name()
        self.scope_stack.append(self.scopes[inner_ns])
        for b in node.bases:
            self.visit(b)
        for stmt in node.body:
            self.visit(stmt)
        self.scope_stack.pop()
        self.name_stack.pop()
        self.class_stack.pop()

    def visit_FunctionDef(self, node):
        message("FunctionDef %s" % (node.name), level=MsgLevel.DEBUG)

#        # Place instance members at class level in the call graph
#        # TODO: brittle: breaks analysis if __init__ defines an internal helper class,
#        # because then the scope lookup will fail. Disabled this special handling for now.
#        if node.name == '__init__':
#            for d in node.args.defaults:
#                self.visit(d)
#            for d in node.args.kw_defaults:
#                self.visit(d)
#            for stmt in node.body:
#                self.visit(stmt)
#            return

        from_node = self.get_current_namespace()
        ns = from_node.get_name()
        to_node = self.get_node(ns, node.name, node)
        if self.add_defines_edge(from_node, to_node):
            message("Def from %s to Function %s" % (from_node, to_node), level=MsgLevel.INFO)

        self.set_value(node.name, to_node)

        self.name_stack.append(node.name)
        inner_ns = self.get_current_namespace().get_name()
        self.scope_stack.append(self.scopes[inner_ns])
        for d in node.args.defaults:
            self.visit(d)
        for d in node.args.kw_defaults:
            self.visit(d)
        for stmt in node.body:
            self.visit(stmt)
        self.scope_stack.pop()
        self.name_stack.pop()

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)  # TODO: alias for now; tag async functions in output in a future version?

    # This gives lambdas their own namespaces in the graph;
    # if that is not desired, this method can be simply omitted.
    #
    # (The default visit() already visits all the children of a generic AST node
    #  by calling generic_visit(); and visit_Name() captures any uses inside the lambda.)
    #
    def visit_Lambda(self, node):
        message("Lambda", level=MsgLevel.DEBUG)
        def process():
            for d in node.args.defaults:
                self.visit(d)
            for d in node.args.kw_defaults:
                self.visit(d)
            self.visit(node.body)  # single expr
        self.with_scope("lambda", process)

    def visit_Import(self, node):
        message("Import %s" % [format_alias(x) for x in node.names], level=MsgLevel.DEBUG)

        # TODO: add support for relative imports (path may be like "....something.something")
        # https://www.python.org/dev/peps/pep-0328/#id10

        for import_item in node.names:
            src_name = import_item.name  # what is being imported
            tgt_name = import_item.asname if import_item.asname is not None else src_name  # under which name

            from_node = self.get_current_namespace()      # where it is being imported to, i.e. the **user**
            to_node  = self.get_node('', tgt_name, node)  # the thing **being used** (under the asname, if any)
            if self.add_uses_edge(from_node, to_node):
                message("Use from %s to Import %s" % (from_node, to_node), level=MsgLevel.INFO)

            # conversion: possible short name -> fully qualified name
            # (when analyzing a set of files in the same directory)
            if src_name in self.module_names:
                mod_name = self.module_names[src_name]
            else:
                mod_name = src_name
            tgt_module = self.get_node('', mod_name, node)
            self.set_value(tgt_name, tgt_module)

    def visit_ImportFrom(self, node):
        message("ImportFrom: from %s import %s" % (node.module, [format_alias(x) for x in node.names]), level=MsgLevel.DEBUG)

        tgt_name = node.module
        from_node = self.get_current_namespace()
        to_node = self.get_node('', tgt_name, node)  # module, in top-level namespace
        if self.add_uses_edge(from_node, to_node):
            message("Use from %s to From %s" % (from_node, to_node), level=MsgLevel.INFO)

        if tgt_name in self.module_names:
            mod_name = self.module_names[tgt_name]
        else:
            mod_name = tgt_name

        for import_item in node.names:
            name = import_item.name
            new_name = import_item.asname if import_item.asname is not None else name
            tgt_id = self.get_node(mod_name, name, node)  # we imported the identifier name from the module mod_name
            self.set_value(new_name, tgt_id)
            message("From setting name %s to %s" % (new_name, tgt_id), level=MsgLevel.INFO)

    # TODO: where are Constants used? (instead of Num, Str, ...)
    def visit_Constant(self, node):
        message("Constant %s" % (node.value), level=MsgLevel.DEBUG)
        t = type(node.value)
        tn = t.__name__
        self.last_value = self.get_node('', tn, node)

    # attribute access (node.ctx determines whether set (ast.Store) or get (ast.Load))
    def visit_Attribute(self, node):
        message("Attribute %s of %s in context %s" % (node.attr, getname(node.value), type(node.ctx)), level=MsgLevel.DEBUG)

        if isinstance(node.ctx, ast.Store):
            # this is the value being assigned (set by visit_Assign())
            save_last_value = self.last_value

            # find the object whose attribute we are accessing
            # (this munges self.last_value to point to the Node for that object)
            #
            self.visit(node.value)

            if isinstance(self.last_value, Node):
                ns = self.ast_node_to_namespace[self.last_value.ast_node]
                if ns in self.scopes:
                    sc = self.scopes[ns]
                    sc.defs[node.attr] = save_last_value
                    message('setattr %s on %s to %s' % (node.attr, self.last_value, save_last_value), level=MsgLevel.INFO)

            self.last_value = save_last_value

        elif isinstance(node.ctx, ast.Load):

            # TODO: add proper support for nested attributes
            #
            # Right now we get, for this code:
            #
            #    class MyClass:
            #        def __init__(self):
            #            class InnerClass:
            #                def __init__(self):
            #                    self.a = 3
            #
            #            self.b = InnerClass()
            #            self.c = self.b.a
            #
            # the following incorrect result:
            #
            #   Assign ['self.c'] ['self.b.a']
            #   Attribute a of self.b in context <class '_ast.Load'>
            #   Get self.b: no Node value (or name not in scope)
            #   AST node <_ast.Attribute object at 0x7f201681b320> (a) has namespace 'None'
            #   Use from <Node testpyan.MyClass.__init__> to Getattr <Node *.a>
            #   Attribute c of self in context <class '_ast.Store'>
            #   Name self in context <class '_ast.Load'>
            #   name self maps to <Node testpyan.MyClass>
            #   setattr c on <Node testpyan.MyClass> to <Node *.a>

            # get our Node object corresponding to node.value in the current ns
            value = self.get_value(getname(node.value))
            # use the original AST node attached to that Node to look up the object's ns
            ns = self.ast_node_to_namespace[value.ast_node] if value is not None else None
            if ns in self.scopes and node.attr in self.scopes[ns].defs:
                result = self.scopes[ns].defs[node.attr]
                message('getattr %s on %s returns %s' % (node.attr, value, result), level=MsgLevel.INFO)
                self.last_value = result
                return

            tgt_name = node.attr
            from_node = self.get_current_namespace()
            if isinstance(self.last_value, Node) and self.last_value.namespace is not None:
                to_node = self.get_node(self.last_value.get_name(), tgt_name, node)
            else:
                to_node = self.get_node(None, tgt_name, node)
            if self.add_uses_edge(from_node, to_node):
                message("Use from %s to Getattr %s" % (from_node, to_node), level=MsgLevel.INFO)

            self.last_value = to_node

    # name access (node.ctx determines whether set (ast.Store) or get (ast.Load))
    def visit_Name(self, node):
        message("Name %s in context %s" % (node.id, type(node.ctx)), level=MsgLevel.DEBUG)

        if isinstance(node.ctx, ast.Store):
            # when we get here, self.last_value has been set by visit_Assign()
            self.set_value(node.id, self.last_value)

        elif isinstance(node.ctx, ast.Load):
            # TODO: we handle self by its name, not by being the first argument in a method
            current_class = self.get_current_class()
            if node.id == 'self' and current_class is not None:
                message('name %s maps to %s' % (node.id, current_class), level=MsgLevel.INFO)
                self.last_value = current_class
                return

            tgt_name = node.id
            from_node = self.get_current_namespace()
            to_node = self.get_value(tgt_name)
            ###TODO if the name is a local variable (i.e. in the innermost scope), and
            ###has no known value, then don't try to create a Node for it.
            if not isinstance(to_node, Node):
                to_node = self.get_node(None, tgt_name, node)  # namespace=None means we don't know the namespace yet
            if self.add_uses_edge(from_node, to_node):
                message("Use from %s to Name %s" % (from_node, to_node), level=MsgLevel.INFO)

            self.last_value = to_node

    def analyze_binding(self, targets, values):
        """Generic handler for binding forms. Inputs must be sanitize()d."""

        # Before we begin analyzing the assignment, clean up any leftover self.last_value.
        #
        # (e.g. from any Name in load context (including function names in a Call)
        #  that did not assign anything.)
        #
        self.last_value = None

        # TODO: properly support tuple unpacking
        #
        #  - the problem is:
        #      a,*b,c = [1,2,3,4,5]  --> Name,Starred,Name = List
        #    so a simple analysis of the AST won't get us far here.
        #
        #  To fix this:
        #
        #  - find the index of Starred on the LHS
        #  - unpack the RHS into a tuple/list (if possible)
        #    - unpack just one level; the items may be tuples/lists and that's just fine
        #    - if not possible to unpack directly (e.g. enumerate(foo) is a **call**),
        #      don't try to be too smart; just do some generic fallback handling
        #  - if RHS unpack successful:
        #    - map the non-starred items directly (one-to-one)
        #    - map the remaining sublist of the RHS to the Starred term
        #      - requires support for tuples/lists of AST nodes as values of Nodes
        #        - but generally, we need that anyway: consider self.a = (f, g, h)
        #          --> any use of self.a should detect the possible use of f, g, and h;
        #              currently this is simply ignored.
        #
        # TODO: support Additional Unpacking Generalizations (Python 3.6+):
        #       https://www.python.org/dev/peps/pep-0448/

        if len(targets) == len(values):  # handle correctly the most common trivial case "a1,a2,... = b1,b2,..."
            for tgt,value in zip(targets,values):
                self.visit(value)  # RHS -> set self.last_value to input for this tgt
                self.visit(tgt)    # LHS
                self.last_value = None
        else:  # FIXME: for now, do the wrong thing in the non-trivial case
            # old code, no tuple unpacking support
            for value in values:
                self.visit(value)  # set self.last_value to **something** on the RHS and hope for the best
            for tgt in targets:    # LHS
                self.visit(tgt)
            self.last_value = None

    def visit_Assign(self, node):
        # - chaining assignments like "a = b = c" produces multiple targets
        # - tuple unpacking works as a separate mechanism on top of that
        #
        if len(node.targets) > 1:
            message("Assign (chained with %d outputs)" % (len(node.targets)), level=MsgLevel.DEBUG)

        values = sanitize(node.value)  # values is the same for each set of targets
        for targets in node.targets:
            targets = sanitize(targets)
            message("Assign %s %s" % ([getname(x) for x in targets], [getname(x) for x in values]), level=MsgLevel.DEBUG)
            self.analyze_binding(targets, values)

    def visit_AnnAssign(self, node):
        self.visit_Assign(self, node)  # TODO: alias for now; add the annotations to output in a future version?

    def visit_AugAssign(self, node):
        targets = sanitize(node.target)
        values = sanitize(node.value)  # values is the same for each set of targets

        message("AugAssign %s %s %s" % ([getname(x) for x in targets], type(node.op), [getname(x) for x in values]), level=MsgLevel.DEBUG)

        # TODO: maybe no need to handle tuple unpacking in AugAssign? (but simpler to use the same implementation)
        self.analyze_binding(targets, values)

    # for() is also a binding form.
    #
    # (Without analyzing the bindings, we would get an unknown node for any
    #  use of the loop counter(s) in the loop body. This can have confusing
    #  consequences in the expand_unknowns() step, if the same name is
    #  in use elsewhere. Thus, we treat for() properly, as a binding form.)
    #
    def visit_For(self, node):
        message("For-loop", level=MsgLevel.DEBUG)

        targets = sanitize(node.target)
        values = sanitize(node.iter)
        self.analyze_binding(targets, values)

        for stmt in node.body:
            self.visit(stmt)
        for stmt in node.orelse:
            self.visit(stmt)

    def visit_AsyncFor(self, node):
        self.visit_For(node)  # TODO: alias for now; tag async for in output in a future version?

    def visit_ListComp(self, node):
        message("ListComp", level=MsgLevel.DEBUG)
        def process():
            self.visit(node.elt)
            self.analyze_generators(node.generators)
        self.with_scope("listcomp", process)

    def visit_SetComp(self, node):
        message("SetComp", level=MsgLevel.DEBUG)
        def process():
            self.visit(node.elt)
            self.analyze_generators(node.generators)
        self.with_scope("setcomp", process)

    def visit_DictComp(self, node):
        message("DictComp", level=MsgLevel.DEBUG)
        def process():
            self.visit(node.key)
            self.visit(node.value)
            self.analyze_generators(node.generators)
        self.with_scope("dictcomp", process)

    def visit_GeneratorExp(self, node):
        message("GeneratorExp", level=MsgLevel.DEBUG)
        def process():
            self.visit(node.elt)
            self.analyze_generators(node.generators)
        self.with_scope("genexpr", process)

    def analyze_generators(self, generators):
        """Analyze the generators in a comprehension form."""
        for gen in generators:
            # TODO: there's also an is_async field we might want to use in a future version.
            targets = sanitize(gen.target)
            values  = sanitize(gen.iter)
            self.analyze_binding(targets, values)

            for expr in gen.ifs:
                self.visit(expr)

    def visit_Call(self, node):
        message("Call %s" % (getname(node.func)), level=MsgLevel.DEBUG)

        for arg in node.args:
            self.visit(arg)
        for kw in node.keywords:
            self.visit(kw.value)

        # Visit the function name part last, so that inside a binding form,
        # it will be left standing as self.last_value.
        self.visit(node.func)

    # TODO: any other interesting AST node types? Full list:
    # https://docs.python.org/3/library/ast.html#abstract-grammar

    def get_node(self, namespace, name, ast_node=None):
        """Return the unique node matching the namespace and name.
        Creates a new node if one doesn't already exist."""

        if name in self.nodes:
            for n in self.nodes[name]:
                if n.namespace == namespace:
                    return n

        n = Node(namespace, name, ast_node)

        # HACK: make the scope info accessible for the visit_*() methods
        # that only have an AST node.
        #
        # In Python 3, symtable and ast are completely separate, so symtable
        # doesn't see our copy of the AST, and symtable's copy of the AST
        # is not accessible from the outside.
        #
        # The visitor only gets an AST, but must be able to access the scope
        # information, so we mediate this by saving the full name of the namespace
        # where each AST node came from when it is get_node()d for the first time.
        #
        if ast_node is not None:
            self.ast_node_to_namespace[ast_node] = namespace
            message("Namespace for AST node %s (%s) recorded as '%s'" % (ast_node, name, namespace), level=MsgLevel.DEBUG)

        if name in self.nodes:
            self.nodes[name].append(n)
        else:
            self.nodes[name] = [n]

        return n

    def get_current_class(self):
        """Return the node representing the current class, or None if not inside a class definition."""
        return self.class_stack[-1] if len(self.class_stack) else None

    def get_current_namespace(self):
        """Return a node representing the current namespace, based on self.name_stack."""

        # namespace nodes do not have an AST node associated with them.

        if not len(self.name_stack):  # the top level is the current module
            return self.get_node('', self.module_name, None)

        namespace = '.'.join(self.name_stack[0:-1])
        name = self.name_stack[-1]
        return self.get_node(namespace, name, None)

    def get_value(self, name):
        """Get the value of name in the current scope. Return None if name is not set to a value."""

        # get the innermost scope that has name **and where name has a value**
        def find_scope(name):
            for sc in reversed(self.scope_stack):
                if name in sc.defs and sc.defs[name] is not None:
                    return sc

        sc = find_scope(name)
        if sc is not None:
            value = sc.defs[name]
            if isinstance(value, Node):
                message('Get %s in %s, found in %s, value %s' % (name, self.scope_stack[-1], sc, value), level=MsgLevel.INFO)
                return value
            else:
                message('Get %s in %s, found in %s: value %s is not a Node' % (name, self.scope_stack[-1], sc, value), level=MsgLevel.DEBUG)
        else:
            message('Get %s in %s: no Node value (or name not in scope)' % (name, self.scope_stack[-1]), level=MsgLevel.DEBUG)
        return None

    def set_value(self, name, value):
        """Set the value of name in the current scope."""

        # get the innermost scope that has name (should be the current scope unless name is a global)
        def find_scope(name):
            for sc in reversed(self.scope_stack):
                if name in sc.defs:
                    return sc

        sc = find_scope(name)
        if sc is not None:
            if isinstance(value, Node):
                sc.defs[name] = value
                message('Set %s in %s to %s' % (name, sc, value), level=MsgLevel.INFO)
            else:
                message('Set %s in %s: value %s is not a Node' % (name, sc, value), level=MsgLevel.DEBUG)
        else:
            message('Set: name %s not in scope' % (name), level=MsgLevel.DEBUG)

    def analyze_scopes(self, code, filename):
        """Gather lexical scope information."""

        # Below, ns is the fully qualified ("dotted") name of sc.
        #
        # Technically, the module scope is anonymous, but we treat it as if
        # it was in a namespace named after the module, to support analysis
        # of several files as a set (keeping their module-level definitions
        # in different scopes, as we should).
        #
        scopes = {}
        def process(parent_ns, table):
            sc = Scope(table)
            ns = "%s.%s" % (parent_ns, sc.name) if len(sc.name) else parent_ns
            scopes[ns] = sc
            for t in table.get_children():
                process(ns, t)
        process(self.module_name, symtable.symtable(code, filename, compile_type="exec"))
        self.scopes = scopes

        message("Scopes: %s" % (scopes), level=MsgLevel.DEBUG)

    def with_scope(self, scopename, thunk):
        """Run thunk (0-argument function) with the scope stack augmented with an inner scope.
        Used to analyze lambda, listcomp et al. (The scope must still be present in self.scopes.)"""
        self.name_stack.append(scopename)
        inner_ns = self.get_current_namespace().get_name()
        self.scope_stack.append(self.scopes[inner_ns])
        thunk()
        self.scope_stack.pop()
        self.name_stack.pop()

    def add_defines_edge(self, from_node, to_node):
        """Add a defines edge in the graph between two nodes.
        N.B. This will mark both nodes as defined."""

        if from_node not in self.defines_edges:
            self.defines_edges[from_node] = set()
        if to_node in self.defines_edges[from_node]:
            return False
        self.defines_edges[from_node].add(to_node)
        from_node.defined = True
        to_node.defined = True
        return True

    def add_uses_edge(self, from_node, to_node):
        """Add a uses edge in the graph between two nodes."""

        if from_node not in self.uses_edges:
            self.uses_edges[from_node] = set()
        if to_node in self.uses_edges[from_node]:
            return False
        self.uses_edges[from_node].add(to_node)
        return True

    def contract_nonexistents(self):
        """For all use edges to non-existent (i.e. not defined nodes) X.name, replace with edge to *.name."""

        new_uses_edges = []
        for n in self.uses_edges:
            for n2 in self.uses_edges[n]:
                if n2.namespace is not None and not n2.defined:
                    n3 = self.get_node(None, n2.name, n2.ast_node)
                    new_uses_edges.append((n, n3))
                    message("Contracting non-existent from %s to %s" % (n, n2), level=MsgLevel.INFO)

        for from_node, to_node in new_uses_edges:
            self.add_uses_edge(from_node, to_node)

    def expand_unknowns(self):
        """For each unknown node *.name, replace all its incoming edges with edges to X.name for all possible Xs."""

        new_defines_edges = []
        for n in self.defines_edges:
            for n2 in self.defines_edges[n]:
                if n2.namespace is None:
                    for n3 in self.nodes[n2.name]:
                        new_defines_edges.append((n, n3))

        for from_node, to_node in new_defines_edges:
            self.add_defines_edge(from_node, to_node)

        new_uses_edges = []
        for n in self.uses_edges:
            for n2 in self.uses_edges[n]:
                if n2.namespace is None:
                    for n3 in self.nodes[n2.name]:
                        new_uses_edges.append((n, n3))

        for from_node, to_node in new_uses_edges:
            self.add_uses_edge(from_node, to_node)

        for name in self.nodes:
            for n in self.nodes[name]:
                if n.namespace is None:
                    n.defined = False

    def cull_inherited(self):
        """For each use edge from W to X.name, if it also has an edge to W to Y.name where Y is used by X, then remove the first edge."""

        removed_uses_edges = []
        for n in self.uses_edges:
            for n2 in self.uses_edges[n]:
                inherited = False
                for n3 in self.uses_edges[n]:
                    if n3.name == n2.name and n2.namespace is not None and n3.namespace is not None and n3.namespace != n2.namespace:
                        if '.' in n2.namespace:
                            nsp2,p2 = n2.namespace.rsplit('.', 1)
                        else:
                            nsp2,p2 = '',n2.namespace
                        if '.' in n3.namespace:
                            nsp3,p3 = n3.namespace.rsplit('.', 1)
                        else:
                            nsp3,p3 = '',n3.namespace
                        pn2 = self.get_node(nsp2, p2, None)
                        pn3 = self.get_node(nsp3, p3, None)
                        if pn2 in self.uses_edges and pn3 in self.uses_edges[pn2]:
                            inherited = True

                if inherited and n in self.uses_edges:
                    removed_uses_edges.append((n, n2))
                    message("Removing inherited edge from %s to %s" % (n, n2), level=MsgLevel.INFO)

        for from_node, to_node in removed_uses_edges:
            self.uses_edges[from_node].remove(to_node)

    def to_dot(self, draw_defines, draw_uses, colored, grouped, nested_groups, annotate):
        if annotate:
            label_node = lambda n: n.get_annotated_name()
        else:
            label_node = lambda n: n.get_short_name()

        # Color nodes by top-level namespace.
        #
        # Use HSL: hue = file, lightness = nesting level.
        #
        # Map top-level namespaces (typically files) to different hues.
        #
        # The "" namespace (for *.py files) gets the first color. Since its
        # level is 0, its lightness will be 1.0, i.e. pure white regardless
        # of the hue.
        #
        class Colorizer:
            def __init__(self, n):
                self._hues = [j/n for j in range(n)]
                self._idx_of = {}  # top-level namespace: hue index
                self._idx = 0

            def _next_idx(self):
                result = self._idx
                self._idx += 1
                if self._idx >= len(self._hues):
                    message("WARNING: colors wrapped", level=MsgLevel.WARNING)
                    self._idx = 0
                return result

            def _get_idx(self, node):
                ns = node.get_toplevel_namespace()
                message("Coloring %s (top-level namespace %s)" % (node.get_short_name(), ns), level=MsgLevel.INFO)
                if ns not in self._idx_of:
                    self._idx_of[ns] = self._next_idx()
                return self._idx_of[ns]

            def get(self, node):  # return (group number, hue)
                idx = self._get_idx(node)
                return (idx,self._hues[idx])

        # find out which nodes are defined (can be visualized)
        vis_node_list = []
        for name in self.nodes:
            for n in self.nodes[name]:
                if n.defined:
                    vis_node_list.append(n)
        # sort by namespace for clustering
        vis_node_list.sort(key=lambda x: x.namespace)

        def find_toplevel_namespaces():
            namespaces = set()
            for node in vis_node_list:
                namespaces.add(node.get_toplevel_namespace())
            return namespaces
        colorizer = Colorizer(n=len(find_toplevel_namespaces())+1)

        s = """digraph G {\n"""

        # enable clustering
        # http://www.graphviz.org/doc/info/attrs.html#a:clusterrank
        if grouped:
            s += """    graph [clusterrank="local"];\n"""

        # Write nodes and subgraphs
        #
        prev_namespace = ""  # The namespace "" (for .py files) is first in vis_node_list.
        namespace_stack = []
        indent = ""
        def update_indent():
            return " " * (4*len(namespace_stack))  # 4 spaces per level
        for n in vis_node_list:
            # new namespace? (NOTE: nodes sorted by namespace!)
            if grouped  and  n.namespace != prev_namespace:
                if nested_groups:
                    # Pop the stack until the newly found namespace is within one of the
                    # parent namespaces (i.e. this is a sibling at that level), or until
                    # the stack runs out.
                    #
                    if len(namespace_stack):
                        m = re.match(namespace_stack[-1], n.namespace)
                        # The '.' check catches siblings in cases like MeshGenerator vs. Mesh.
                        while m is None  or  n.namespace[m.end()] != '.':
                            s += """%s}\n""" % indent  # terminate previous subgraph
                            namespace_stack.pop()
                            indent = update_indent()
                            if not len(namespace_stack):
                                break
                            m = re.match(namespace_stack[-1], n.namespace)
                    namespace_stack.append(n.namespace)
                    indent = update_indent()
                else:
                    if prev_namespace != "":
                        s += """%s}\n""" % indent  # terminate previous subgraph
                    else:
                        indent = " " * 4  # first subgraph begins, start indenting
                prev_namespace = n.namespace
                # Begin new subgraph for this namespace (TODO: refactor the label generation).
                #
                # Name must begin with "cluster" to be recognized as a cluster by GraphViz.
                s += """%ssubgraph cluster_%s {\n""" % (indent, n.namespace.replace('.', '__').replace('*', ''))

                # translucent gray (no hue to avoid visual confusion with any group of colored nodes)
                s += """%s    graph [style="filled,rounded", fillcolor="#80808018", label="%s"];\n""" % (indent, n.namespace)

            # add the node itself
            if colored:
                idx,H = colorizer.get(n)
                S = 1.0
                L = max( [1.0 - 0.1*n.get_level(), 0.1] )
                A = 0.7  # make nodes translucent (to handle possible overlaps)
                fill_RGBA = htmlize_rgb(*hsl2rgb(H,S,L), A=A)

                if L >= 0.5:
                    text_RGB = htmlize_rgb(0.0, 0.0, 0.0)  # black text on light nodes
                else:
                    text_RGB = htmlize_rgb(1.0, 1.0, 1.0)  # white text on dark nodes

                s += """%s    %s [label="%s", style="filled", fillcolor="%s", fontcolor="%s", group="%s"];\n""" % (indent, n.get_label(), label_node(n), fill_RGBA, text_RGB, idx)
            else:
                fill_RGBA = htmlize_rgb(1.0, 1.0, 1.0, 0.7)
                idx,_ = colorizer.get(n)
                s += """%s    %s [label="%s", style="filled", fillcolor="%s", fontcolor="#000000", group="%s"];\n""" % (indent, n.get_label(), label_node(n), fill_RGBA, idx)

        if grouped:
            if nested_groups:
                while len(namespace_stack):
                    s += """%s}\n""" % indent  # terminate all remaining subgraphs
                    namespace_stack.pop()
                    indent = update_indent()
            else:
                s += """%s}\n""" % indent  # terminate last subgraph

        # Write defines relationships
        #
        if draw_defines:
            for n in self.defines_edges:
                if n.defined:
                    for n2 in self.defines_edges[n]:
                        if n2.defined and n2 != n:
                            # gray lines (so they won't visually obstruct the "uses" lines)
                            s += """    %s -> %s [style="dashed", color="azure4"];\n""" % (n.get_label(), n2.get_label())

        # Write uses relationships
        #
        if draw_uses:
            for n in self.uses_edges:
                if n.defined:
                    for n2 in self.uses_edges[n]:
                        if n2.defined and n2 != n:
                            s += """    %s -> %s;\n""" % (n.get_label(), n2.get_label())

        s += """}\n"""  # terminate "digraph G {"
        return s


    def to_tgf(self, draw_defines, draw_uses):
        s = ''
        i = 1
        id_map = {}
        for name in self.nodes:
            for n in self.nodes[name]:
                if n.defined:
                    s += """%d %s\n""" % (i, n.get_short_name())
                    id_map[n] = i
                    i += 1
                #else:
                #    print("ignoring %s" % n, file=sys.stderr)

        s += """#\n"""

        if draw_defines:
            for n in self.defines_edges:
                if n.defined:
                    for n2 in self.defines_edges[n]:
                        if n2.defined and n2 != n:
                            i1 = id_map[n]
                            i2 = id_map[n2]
                            s += """%d %d D\n""" % (i1, i2)

        if draw_uses:
            for n in self.uses_edges:
                if n.defined:
                    for n2 in self.uses_edges[n]:
                        if n2.defined and n2 != n:
                            i1 = id_map[n]
                            i2 = id_map[n2]
                            s += """%d %d U\n""" % (i1, i2)
        return s


def main():
    usage = """usage: %prog FILENAME... [--dot|--tgf]"""
    desc = """Analyse one or more Python source files and generate an approximate call graph of the modules, classes and functions within them."""
    parser = OptionParser(usage=usage, description=desc)
    parser.add_option("--dot",
                      action="store_true", default=False,
                      help="output in GraphViz dot format")
    parser.add_option("--tgf",
                      action="store_true", default=False,
                      help="output in Trivial Graph Format")
    parser.add_option("-v", "--verbose",
                      action="store_true", default=False, dest="verbose",
                      help="verbose output")
    parser.add_option("-V", "--very-verbose",
                      action="store_true", default=False, dest="very_verbose",
                      help="even more verbose output (mainly for debug)")
    parser.add_option("-d", "--defines",
                      action="store_true", default=True, dest="draw_defines",
                      help="add edges for 'defines' relationships [default]")
    parser.add_option("-n", "--no-defines",
                      action="store_false", default=True, dest="draw_defines",
                      help="do not add edges for 'defines' relationships")
    parser.add_option("-u", "--uses",
                      action="store_true", default=True, dest="draw_uses",
                      help="add edges for 'uses' relationships [default]")
    parser.add_option("-N", "--no-uses",
                      action="store_false", default=True, dest="draw_uses",
                      help="do not add edges for 'uses' relationships")
    parser.add_option("-c", "--colored",
                      action="store_true", default=False, dest="colored",
                      help="color nodes according to namespace [dot only]")
    parser.add_option("-g", "--grouped",
                      action="store_true", default=False, dest="grouped",
                      help="group nodes (create subgraphs) according to namespace [dot only]")
    parser.add_option("-e", "--nested-groups",
                      action="store_true", default=False, dest="nested_groups",
                      help="create nested groups (subgraphs) for nested namespaces (implies -g) [dot only]")
    parser.add_option("-a", "--annotate",
                      action="store_true", default=False, dest="annotate",
                      help="annotate with module and source line number [dot only]")

    options, args = parser.parse_args()
    filenames = [fn2 for fn in args for fn2 in glob(fn)]
    if len(args) == 0:
        parser.error('Need one or more filenames to process')

    if options.nested_groups:
        options.grouped = True

    # TODO: use an int argument
    global verbosity
    if options.very_verbose:
        verbosity = MsgLevel.DEBUG
    elif options.verbose:
        verbosity = MsgLevel.INFO

    # Process the set of files, TWICE: so that forward references are picked up
    v = CallGraphVisitor(filenames)
    for pas in range(2):
        for filename in filenames:
            message("========== pass %d for file '%s' ==========" % (pas+1, filename), level=MsgLevel.INFO)
            v.process(filename)
    v.postprocess()

    if options.dot:
        print(v.to_dot(draw_defines=options.draw_defines,
                       draw_uses=options.draw_uses,
                       colored=options.colored,
                       grouped=options.grouped,
                       nested_groups=options.nested_groups,
                       annotate=options.annotate))
    if options.tgf:
        print(v.to_tgf(draw_defines=options.draw_defines,
                       draw_uses=options.draw_uses))


if __name__ == '__main__':
    main()
