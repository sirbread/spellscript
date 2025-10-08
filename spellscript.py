import re
import sys
import time

class SpellScriptInterpreter:
    def __init__(self):
        self.variables = {}
        self.tokens = []

    def tokenize(self, spell_text):
        spell_text = re.sub(r'\s+', ' ', spell_text).strip()
        statements = re.split(r'(?<=\.)\s*', spell_text)
        return [s.strip() for s in statements if s.strip()]

    def parse_and_execute(self, spell_text):
        self.tokens = self.tokenize(spell_text)
        if not self.tokens:
            raise SyntaxError("empty spell")
        first = self.tokens[0].lower()
        last = self.tokens[-1].lower()
        if "begin the grimoire" not in first:
            raise SyntaxError("spells must begin with Begin the grimoire")
        if "close the grimoire" not in last:
            raise SyntaxError("spells must end with Close the grimoire")
        for stmt in self.tokens[1:-1]:
            self.execute_statement(stmt)

    def execute_statement(self, statement):
        statement = statement.strip()
        if statement.endswith('.'):
            statement = statement[:-1]
        if not statement:
            return
        words = statement.split()
        cmd = words[0].lower()
        if cmd == "summon":
            self.handle_summon(statement)
        elif cmd == "enchant":
            self.handle_enchant(statement)
        elif cmd == "inscribe":
            self.handle_inscribe(statement)
        elif cmd == "ponder":
            self.handle_ponder(words)
        else:
            raise SyntaxError(f"unknown incantation {cmd}")

    def handle_summon(self, statement):
        parts = statement.split()
        if len(parts) < 3 or parts[1].lower() != "the":
            raise SyntaxError("use Summon the <name> [with essence of <value>]")
        name = parts[2]
        if "with essence of" in statement:
            idx = statement.find("with essence of") + len("with essence of")
            val = self.evaluate_expression(statement[idx:].strip())
        else:
            val = None
        self.variables[name] = val

    def handle_enchant(self, statement):
        parts = statement.split()
        if len(parts) < 3:
            raise SyntaxError("use Enchant <name> with <value>")
        name = parts[1]
        if "with" not in statement:
            raise SyntaxError("enchant requires with")
        idx = statement.find("with") + len("with")
        val = self.evaluate_expression(statement[idx:].strip())
        if name not in self.variables:
            raise NameError(f"unknown entity {name}")
        self.variables[name] = val

    def handle_inscribe(self, statement):
        msg = statement[len("inscribe "):].strip()
        if msg in self.variables:
            print(self.variables[msg])
            return
        if msg.startswith('whispers of "') and msg.endswith('"'):
            print(msg[len('whispers of "'): -1])
            return
        print(msg)

    def handle_ponder(self, words):
        if len(words) >= 3 and words[1] == "for" and words[2].isdigit():
            time.sleep(float(words[2]))
        else:
            raise SyntaxError("use Ponder for <seconds> moments")

    def evaluate_expression(self, expr):
        expr = expr.strip()
        if expr in self.variables:
            return self.variables[expr]
        try:
            if '.' in expr:
                return float(expr)
            return int(expr)
        except ValueError:
            pass
        if expr == "truth":
            return True
        if expr == "falsehood":
            return False
        if expr.startswith('whispers of "') and expr.endswith('"'):
            return expr[len('whispers of "'): -1]
        return expr

def main():
    if len(sys.argv) < 2:
        print("usage python spellscript.py <spell_filename>.spell")
        sys.exit(1)
    with open(sys.argv[1], 'r') as f:
        text = f.read()
    interp = SpellScriptInterpreter()
    try:
        interp.parse_and_execute(text)
    except Exception as e:
        print(f"the spell has backfired: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

