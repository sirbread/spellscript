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
        lower = statement.lower()
        if "if the signs show" in lower:
            self.handle_conditional(statement)
            return
        if "repeat the incantation" in lower:
            self.handle_loop(statement)
            return
        words = statement.split()
        if not words:
            return
        cmd = words[0].lower()
        if cmd == "summon":
            self.handle_summon(statement)
        elif cmd == "enchant":
            self.handle_enchant(statement)
        elif cmd == "inscribe":
            self.handle_inscribe(statement)
        elif cmd == "ponder":
            self.handle_ponder(words)
        elif cmd == "banish":
            self.handle_banish(words)
        elif cmd == "gaze":
            self.handle_gaze(words)
        elif cmd == "transmute":
            self.handle_transmute(words)
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
            print(msg[len('whispers of "'):-1])
            return
        print(msg)

    def handle_ponder(self, words):
        if len(words) >= 4 and words[1] == "for" and words[3] == "moments":
            try:
                time.sleep(float(words[2]))
            except ValueError:
                raise SyntaxError("ponder duration must be a number")
        else:
            raise SyntaxError("use Ponder for <seconds> moments")

    def handle_conditional(self, statement):
        lower = statement.lower()
        start = lower.find("if the signs show") + len("if the signs show")
        end = lower.find("then")
        if end == -1:
            raise SyntaxError("conditional must include then")
        cond = statement[start:end].strip()
        act = statement[end + len("then"):].strip()
        if self.evaluate_condition(cond):
            self.execute_statement(act)

    def handle_loop(self, statement):
        match = re.search(r'repeat the incantation (\d+) times', statement.lower())
        if not match:
            raise SyntaxError("use Repeat the incantation <number> times do <action>")
        count = int(match.group(1))
        if "do" not in statement.lower():
            raise SyntaxError("loop requires 'do' clause")
        action_start = statement.lower().find("do") + len("do")
        action = statement[action_start:].strip()
        for _ in range(count):
            self.execute_statement(action)

    def handle_banish(self, words):
        if len(words) < 3 or words[1].lower() != "the":
            raise SyntaxError("use Banish the <name>")
        name = words[2]
        if name in self.variables:
            del self.variables[name]
        else:
            raise NameError(f"cannot banish unknown entity {name}")

    def handle_gaze(self, words):
        if len(words) < 3 or words[1].lower() != "upon":
            raise SyntaxError("use Gaze upon <condition>")
        condition = " ".join(words[2:])
        result = self.evaluate_condition(condition)
        print(f"Gazing reveals: {result}")

    def handle_transmute(self, words):
        if len(words) < 5 or words[2].lower() != "into":
            raise SyntaxError("use Transmute <name> into <type>")
        var_name = words[1]
        target_type = words[3].lower()
        if var_name not in self.variables:
            raise NameError(f"cannot transmute unknown entity {var_name}")
        value = self.variables[var_name]
        try:
            if target_type == "number":
                self.variables[var_name] = float(value) if '.' in str(value) else int(value)
            elif target_type == "text":
                self.variables[var_name] = str(value)
            elif target_type == "truth":
                self.variables[var_name] = bool(value)
            else:
                raise ValueError(f"unknown transmutation target {target_type}")
        except Exception as e:
            raise ValueError(f"failed to transmute {var_name}: {e}")

    def evaluate_condition(self, condition):
        cond = condition.lower().strip()
        if "equals" in cond:
            a, b = cond.split("equals", 1)
            return self.evaluate_expression(a.strip()) == self.evaluate_expression(b.strip())
        if "greater than" in cond:
            a, b = cond.split("greater than", 1)
            return self.evaluate_expression(a.strip()) > self.evaluate_expression(b.strip())
        if "less than" in cond:
            a, b = cond.split("less than", 1)
            return self.evaluate_expression(a.strip()) < self.evaluate_expression(b.strip())
        if cond == "truth":
            return True
        if cond == "falsehood":
            return False
        if cond in self.variables:
            return bool(self.variables[cond])
        return False

    def evaluate_expression(self, expr):
        expr = expr.strip()
        if "greater by" in expr:
            a, b = expr.split("greater by", 1)
            return self.evaluate_expression(a.strip()) + self.evaluate_expression(b.strip())
        if "lesser by" in expr:
            a, b = expr.split("lesser by", 1)
            return self.evaluate_expression(a.strip()) - self.evaluate_expression(b.strip())


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
            return expr[len('whispers of "'):-1]
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

