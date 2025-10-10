import re
import sys
import time

class SpellScriptInterpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.tokens = []
        self.current_token_index = 0
        self.last_return_value = None

    def tokenize(self, spell_text):
        pattern = r'((?:[^\."]|"[^"]*")+\.)'
        statements = re.findall(pattern, spell_text)
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
        
        self.current_token_index = 1
        while self.current_token_index < len(self.tokens) - 1:
            statement = self.tokens[self.current_token_index]
            self.current_token_index += 1
            self.execute_statement(statement)

    def remove_filler_words(self, text):
        text = re.sub(r'\bis\b', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

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
            self.handle_transmute(statement)
        elif cmd == "conjure":
            self.handle_conjure(statement)
        elif cmd == "invoke":
            return self.handle_invoke(statement)
        elif cmd == "return":
            return self.handle_return(statement)
        else:
            raise SyntaxError(f"unknown incantation {cmd}")

    def handle_summon(self, statement):
        parts = statement.split()
        if len(parts) < 3 or parts[1].lower() != "the":
            raise SyntaxError("use Summon the <name> [with essence of <value>] or [through ritual <name> with <args>]")
        name = parts[2]
        
        if "through ritual" in statement.lower():
            idx = statement.lower().find("through ritual") + len("through ritual")
            ritual_call = statement[idx:].strip()
            val = self.evaluate_ritual_call(ritual_call)
        elif "with essence of" in statement:
            idx = statement.find("with essence of") + len("with essence of")
            val = self.evaluate_expression(statement[idx:].strip())
        else:
            val = None
        self.variables[name] = val

    def handle_enchant(self, statement):
        pattern = r'Enchant\s+(\w+)\s+(.+)'
        match = re.match(pattern, statement, re.IGNORECASE)
        if not match:
            raise SyntaxError("use Enchant <name> with <value> or through ritual <name> with <args>")
        name = match.group(1)
        rest = match.group(2).strip()
        
        if name not in self.variables:
            raise NameError(f"unknown entity {name}")
        
        if rest.lower().startswith("through ritual"):
            ritual_call = rest[len("through ritual"):].strip()
            val = self.evaluate_ritual_call(ritual_call)
        elif rest.lower().startswith("with"):
            expr = rest[len("with"):].strip()
            val = self.evaluate_expression(expr)
        else:
            raise SyntaxError("use Enchant <name> with <value> or through ritual <name> with <args>")

        self.variables[name] = val

    def evaluate_ritual_call(self, ritual_call):
        pattern = r'(\w+)(?: with (.+))?'
        match = re.match(pattern, ritual_call, re.IGNORECASE)
        if not match:
            raise SyntaxError("invalid ritual call syntax")

        name = match.group(1)
        args_str = match.group(2)

        if name not in self.functions:
            raise NameError(f"ritual {name} not found")

        func = self.functions[name]
        params = func["params"]

        if args_str:
            args_raw = [a.strip() for a in args_str.split("and")]
            args = []
            arg_var_names = []

            for arg in args_raw:
                if arg in self.variables:
                    arg_var_names.append(arg)
                    args.append(self.variables[arg])
                else:
                    arg_var_names.append(None)
                    args.append(self.evaluate_expression(arg))
        else:
            args = []
            arg_var_names = []

        if len(args) != len(params):
            raise ValueError(f"ritual {name} expects {len(params)} args, got {len(args)}")

        saved_param_values = {}
        for p in params:
            if p in self.variables:
                saved_param_values[p] = self.variables[p]

        for p, a in zip(params, args):
            self.variables[p] = a

        result = self.execute_statement(func["body"])

        for i, (param, var_name) in enumerate(zip(params, arg_var_names)):
            if var_name is not None and param in self.variables:
                self.variables[var_name] = self.variables[param]

        for p in params:
            if p in saved_param_values:
                self.variables[p] = saved_param_values[p]
            else:
                if p in self.variables:
                    del self.variables[p]

        return result

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
                duration = self.parse_number(words[2])
                time.sleep(duration)
            except ValueError:
                raise SyntaxError("ponder duration must be a number")
        else:
            raise SyntaxError("use Ponder for <seconds> moments")

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

    def handle_transmute(self, statement):
        if " into " not in statement.lower():
            raise SyntaxError("use Transmute <name> into <type>")

        parts = re.split(r'\s+into\s+', statement, flags=re.IGNORECASE, maxsplit=1)
        if len(parts) != 2:
            raise SyntaxError("use Transmute <name> into <type>")

        var_part = parts[0].strip()
        if var_part.lower().startswith("transmute "):
            var_name = var_part[len("transmute "):].strip()
        else:
            raise SyntaxError("use Transmute <name> into <type>")

        target_type = parts[1].strip().lower()

        if var_name in self.variables:
            value = self.variables[var_name]
        else:
            value = self.evaluate_expression(var_name)

        try:
            if target_type == "number":
                if isinstance(value, str) and 'point' in value.lower():
                    value = self.parse_number(value)
                else:
                    value = float(value) if '.' in str(value) else int(value)
            elif target_type == "text":
                value = str(value)
            elif target_type == "truth":
                value = bool(value)
            else:
                raise ValueError(f"unknown transmutation target {target_type}")
        except Exception as e:
            raise ValueError(f"failed to transmute {var_name}: {e}")

        self.variables[var_name] = value
        return value

    def handle_conjure(self, statement):
        pattern = r'Conjure ritual named (\w+) with (.+?) to (.+)'
        match = re.match(pattern, statement, re.IGNORECASE)
        if not match:
            raise SyntaxError("use Conjure ritual named <name> with <params> to <body>")
        name, params_str, body = match.groups()
        params = [p.strip() for p in params_str.split("and")]
        body = body.strip()
        if body.endswith('.'):
            body = body[:-1].strip()
        self.functions[name] = {
            "params": params,
            "body": body
        }

    def handle_return(self, statement):
        parts = statement.split(maxsplit=1)
        if len(parts) < 2:
            raise SyntaxError("use Return <value>")
        value_expr = parts[1].strip()
        return self.evaluate_expression(value_expr)

    def handle_invoke(self, statement):
        pattern = r'Invoke the ritual (\w+)(?: with (.+))?'
        match = re.match(pattern, statement, re.IGNORECASE)
        if not match:
            raise SyntaxError("use Invoke the ritual <name> with <args>")
        name, args_str = match.groups()
        if name not in self.functions:
            raise NameError(f"ritual {name} not found")
        func = self.functions[name]
        params = func["params"]
        if args_str:
            args_raw = [a.strip() for a in args_str.split("and")]
            args = []
            arg_var_names = []
            
            for arg in args_raw:
                if arg in self.variables:
                    arg_var_names.append(arg)
                    args.append(self.variables[arg])
                else:
                    arg_var_names.append(None)
                    args.append(self.evaluate_expression(arg))
        else:
            args = []
            arg_var_names = []
            
        if len(args) != len(params):
            raise ValueError(f"ritual {name} expects {len(params)} args, got {len(args)}")
        
        saved_param_values = {}
        for p in params:
            if p in self.variables:
                saved_param_values[p] = self.variables[p]
        
        for p, a in zip(params, args):
            self.variables[p] = a
        
        result = self.execute_statement(func["body"])
        
        for i, (param, var_name) in enumerate(zip(params, arg_var_names)):
            if var_name is not None and param in self.variables:
                self.variables[var_name] = self.variables[param]
        
        for p in params:
            if p in saved_param_values:
                self.variables[p] = saved_param_values[p]
            else:
                if p in self.variables:
                    del self.variables[p]
        
        self.last_return_value = result
        return result

    def handle_conditional(self, statement):
        lower = statement.lower()
        start = lower.find("if the signs show") + len("if the signs show")
        then_pos = lower.find("then")
        if then_pos == -1:
            raise SyntaxError("conditional must include then")

        cond = statement[start:then_pos].strip()
        cond = self.remove_filler_words(cond)

        otherwise_pos = lower.find(" otherwise ")

        if otherwise_pos != -1:
            then_action = statement[then_pos + len("then"):otherwise_pos].strip()
            else_action = statement[otherwise_pos + len(" otherwise "):].strip()

            if self.evaluate_condition(cond):
                return self.execute_statement(then_action)
            else:
                return self.execute_statement(else_action)
        else:
            then_action = statement[then_pos + len("then"):].strip()
            if self.evaluate_condition(cond):
                return self.execute_statement(then_action)

    def handle_loop(self, statement):
        statement = statement.strip()
        match = re.search(r'repeat the incantation (\d+) times', statement.lower())
        if not match:
            raise SyntaxError("use Repeat the incantation <number> times do <action>")
        count = int(match.group(1))
        
        body_tokens = []
        if "do" in statement.lower():
            do_pos = statement.lower().find("do") + 2
            body_text = statement[do_pos:].strip()
            if body_text:
                body_statements = re.split(r'\.\s+', body_text)
                for s in body_statements:
                    s = s.strip()
                    if s.endswith('.'):
                        s = s[:-1].strip()
                    if s:
                        body_tokens.append(s)
        
        while self.current_token_index < len(self.tokens) - 1:
            token = self.tokens[self.current_token_index]
            token = token.strip()
            if token.endswith('.'):
                token = token[:-1]
            token = token.strip()
            
            if token.lower() == "end loop":
                self.current_token_index += 1
                break
            
            if token:
                body_tokens.append(token)
            self.current_token_index += 1
        

        if not body_tokens:
            raise SyntaxError("loop body is empty")
        
        for _ in range(count):
            for action_statement in body_tokens:
                self.execute_statement(action_statement)

    def parse_number(self, text):
        text = text.strip()
        
        if 'point' in text.lower():
            text = re.sub(r'point', '.', text, flags=re.IGNORECASE)
        
        try:
            num = float(text)
            if num.is_integer():
                return int(num)
            return num
        except ValueError:
            raise ValueError(f"Cannot parse '{text}' as a number")

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
        
        if "through ritual" in expr.lower():
            pattern = r'through ritual (.+)'
            match = re.search(pattern, expr, re.IGNORECASE)
            if match:
                ritual_call = match.group(1).strip()
                return self.evaluate_ritual_call(ritual_call)

        if "invoke the ritual" in expr.lower():
            pattern = r'invoke the ritual (\w+)(?: with (.+))?'
            match = re.search(pattern, expr, re.IGNORECASE)
            if match:
                invoke_start = match.start()
                invoke_end = match.end()

                result = self.handle_invoke(expr[invoke_start:invoke_end])

                remaining = expr[:invoke_start] + str(result) + expr[invoke_end:]
                remaining = remaining.strip()

                if remaining and remaining != str(result):
                    return self.evaluate_expression(remaining)

                return result
        
        if "greater by" in expr.lower():
            parts = re.split(r'\s+greater by\s+', expr, flags=re.IGNORECASE, maxsplit=1)
            if len(parts) == 2:
                a = self.evaluate_expression(parts[0].strip())
                b = self.evaluate_expression(parts[1].strip())
                if not isinstance(a, (int, float)):
                    raise TypeError(f"Expected number, got {type(a).__name__}: {a}")
                if not isinstance(b, (int, float)):
                    raise TypeError(f"Expected number, got {type(b).__name__}: {b}")
                return a + b
        
        if "lesser by" in expr.lower():
            parts = re.split(r'\s+lesser by\s+', expr, flags=re.IGNORECASE, maxsplit=1)
            if len(parts) == 2:
                a = self.evaluate_expression(parts[0].strip())
                b = self.evaluate_expression(parts[1].strip())
                if not isinstance(a, (int, float)):
                    raise TypeError(f"Expected number, got {type(a).__name__}: {a}")
                if not isinstance(b, (int, float)):
                    raise TypeError(f"Expected number, got {type(b).__name__}: {b}")
                return a - b
        
        if "multiplied by" in expr.lower():
            parts = re.split(r'\s+multiplied by\s+', expr, flags=re.IGNORECASE, maxsplit=1)
            if len(parts) == 2:
                a = self.evaluate_expression(parts[0].strip())
                b = self.evaluate_expression(parts[1].strip())
                if not isinstance(a, (int, float)):
                    raise TypeError(f"Expected number, got {type(a).__name__}: {a}")
                if not isinstance(b, (int, float)):
                    raise TypeError(f"Expected number, got {type(b).__name__}: {b}")
                return a * b

        if "divided by" in expr.lower():
            parts = re.split(r'\s+divided by\s+', expr, flags=re.IGNORECASE, maxsplit=1)
            if len(parts) == 2:
                a = self.evaluate_expression(parts[0].strip())
                b = self.evaluate_expression(parts[1].strip())
                if not isinstance(a, (int, float)):
                    raise TypeError(f"Expected number, got {type(a).__name__}: {a}")
                if not isinstance(b, (int, float)):
                    raise TypeError(f"Expected number, got {type(b).__name__}: {b}")
                if b == 0:
                    raise ZeroDivisionError("Cannot divide by zero")
                result = a / b
                if isinstance(a, int) and isinstance(b, int) and result.is_integer():
                    return int(result)
                return result


        if expr in self.variables:
            return self.variables[expr]
        
        try:
            return self.parse_number(expr)
        except ValueError:
            pass
        
        if expr.lower() == "truth":
            return True
        if expr.lower() == "falsehood":
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