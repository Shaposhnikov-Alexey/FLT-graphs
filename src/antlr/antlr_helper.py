from antlr4 import *
from antlr4.error.Errors import ParseCancellationException
from antlr4.error.ErrorListener import ErrorListener
from antlr4.tree.Tree import Tree
from antlr4.tree.Trees import Trees
from antlr4.tree.Tree import TerminalNodeImpl

from src.antlr.db_grammarLexer import db_grammarLexer
from src.antlr.db_grammarListener import db_grammarListener
from src.antlr.db_grammarParser import db_grammarParser
from graphviz import Digraph


class TreeWalker(db_grammarListener):
    def __init__(self, view: Digraph):
        self.view = view
        self.counter = 0
        self.node_to_id = {}
        super(db_grammarListener, self).__init__()

    def enterEveryRule(self, context: ParserRuleContext):
        if context not in self.node_to_id:
            self.view.node(self.get_node_id(context), label=self.get_node_name(context))
        for child in context.children:
            self.view.node(self.get_node_id(child), label=self.get_node_name(child))
            self.view.edge(self.get_node_id(context), self.get_node_id(child))

    def get_node_id(self, node: ParserRuleContext):
        if node not in self.node_to_id:
            self.node_to_id[node] = self.counter
            self.counter += 1
        return str(self.node_to_id[node])

    def get_node_name(self, context: ParserRuleContext):
        if isinstance(context, TerminalNodeImpl):
            return context.symbol.text
        else:
            return str(type(context).__name__).replace('Context', '').lower()


class TreeHelper:
    def __init__(self, input: InputStream):
        lexer = db_grammarLexer(input)
        stream = CommonTokenStream(lexer)
        parser = db_grammarParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(self.GrammarErrorListener)
        try:
            self.tree = parser.script()
        except ParseCancellationException:
            self.tree = None

    class GrammarErrorListener(ErrorListener):
        @staticmethod
        def syntaxError(recognizer, offending_symbol, line, column, msg, e):
            print(f'Error on {line} line with: {msg}\n offending symbol: {offending_symbol}')
            raise ParseCancellationException(f"line: {line} msg: {msg}")

    def get_visualization(self, output_file, show_view=True):
        view = Digraph(comment="DBQL AST")
        if self.tree is not None:
            ParseTreeWalker().walk(TreeWalker(view), self.tree)
            view.render(output_file, view=show_view)
        else:
            print("Parsing finished with errors")
