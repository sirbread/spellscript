# spellscript interpreter
# open sourced and documented at: https://github.com/sirbread/spellscript

import re
import sys
import time

class ExecutionContext:
    def __init__(self, source='main', body_statements=None, start_index=0):
        self.source = source
        self.body_statements = body_statements or []
        self.current_index = start_index

class SpellScriptInterpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.tokens = []
        self.current_token_index = 0
        self.last_return_value = None
        self.context_stack = []

    def tokenize(self, spell_text):
        pattern = r'((?:[^\.":"]|"[^"]*")+[\.:])'
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
        if statement.endswith('.') or statement.endswith(':'):
            statement = statement[:-1]
        if not statement:
            return
        lower = statement.lower()
        if "if the signs show" in lower:
            return self.handle_conditional(statement)
        if "repeat the incantation" in lower:
            return self.handle_loop(statement)
        if lower.startswith("traverse "):
            return self.handle_traverse(statement)
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
        elif cmd == "inquire":
            self.handle_inquire(statement)
        elif cmd == "append":
            self.handle_append(statement)
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
            raise SyntaxError("use Summon the <name> [with essence of <value>]")
        name = parts[2]
        
        if "with essence of" in statement:
            idx = statement.find("with essence of") + len("with essence of")
            val = self.evaluate_expression(statement[idx:].strip())
        else:
            val = None
        self.variables[name] = val

    def handle_enchant(self, statement):
        if " at position " in statement.lower():
            pattern = r'Enchant\s+(\w+)\s+at position\s+(.+?)\s+with\s+(.+)'
            match = re.match(pattern, statement, re.IGNORECASE)
            if not match:
                raise SyntaxError("use Enchant <array> at position <index> with <value>")
            
            array_name = match.group(1)
            index_expr = match.group(2).strip()
            value_expr = match.group(3).strip()
            
            if array_name not in self.variables:
                raise NameError(f"unknown entity {array_name}")
            
            array = self.variables[array_name]
            if not isinstance(array, list):
                raise TypeError(f"{array_name} is not a collection")
            
            index = self.evaluate_expression(index_expr)
            if not isinstance(index, int):
                raise TypeError(f"index must be a number, got {type(index).__name__}")
            
            value = self.evaluate_expression(value_expr)
            
            if index < 0 or index >= len(array):
                raise IndexError(f"index {index} out of range for collection of length {len(array)}")
            
            array[index] = value
            return
        
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

    def handle_inquire(self, statement):
        pattern = r'Inquire\s+whispers of\s+"([^"]*)"\s+into\s+(\w+)'
        match = re.match(pattern, statement, re.IGNORECASE)
        if not match:
            raise SyntaxError('use Inquire whispers of "prompt" into <name>')

        prompt = match.group(1)
        var_name = match.group(2)
        user_input = input(prompt + " ")
        self.variables[var_name] = user_input

    def handle_append(self, statement):
        pattern = r'Append\s+(.+?)\s+to\s+(\w+)'
        match = re.match(pattern, statement, re.IGNORECASE)
        if not match:
            raise SyntaxError("use Append <value> to <array>")
        
        value_expr = match.group(1).strip()
        array_name = match.group(2).strip()
        
        if array_name not in self.variables:
            raise NameError(f"unknown entity {array_name}")
        
        array = self.variables[array_name]
        if not isinstance(array, list):
            raise TypeError(f"{array_name} is not a collection")
        
        value = self.evaluate_expression(value_expr)
        array.append(value)

    def collect_block_from_context(self, end_keyword):
        body_statements = []
        depth = 0
        
        if end_keyword == "end loop":
            start_patterns = ["repeat the incantation"]
        elif end_keyword == "end traverse":
            start_patterns = ["traverse "]
        elif end_keyword == "end ritual":
            start_patterns = ["conjure ritual named"]
        else:
            start_patterns = []
        
        if self.context_stack:
            context = self.context_stack[-1]
            while context.current_index < len(context.body_statements):
                token = context.body_statements[context.current_index]
                context.current_index += 1
                
                token = token.strip()
                if token.endswith('.') or token.endswith(':'):
                    token = token[:-1]
                token = token.strip()
                
                token_lower = token.lower()
                
                is_start = any(pattern in token_lower for pattern in start_patterns)
                if is_start and "to begin" in token_lower:
                    depth += 1
                    body_statements.append(token)
                elif token_lower == end_keyword:
                    if depth == 0:
                        break
                    else:
                        depth -= 1
                        body_statements.append(token)
                elif token:
                    body_statements.append(token)
        else:
            while self.current_token_index < len(self.tokens) - 1:
                token = self.tokens[self.current_token_index]
                self.current_token_index += 1
                
                token = token.strip()
                if token.endswith('.') or token.endswith(':'):
                    token = token[:-1]
                token = token.strip()
                
                token_lower = token.lower()
                
                is_start = any(pattern in token_lower for pattern in start_patterns)
                if is_start and "to begin" in token_lower:
                    depth += 1
                    body_statements.append(token)
                elif token_lower == end_keyword:
                    if depth == 0:
                        break
                    else:
                        depth -= 1
                        body_statements.append(token)
                elif token:
                    body_statements.append(token)
        
        return body_statements

    def handle_traverse(self, statement):
        pattern_with_index = r'Traverse\s+(\w+)\s+with each\s+(\w+)\s+at\s+(\w+)\s+to begin'
        pattern_simple = r'Traverse\s+(\w+)\s+with each\s+(\w+)\s+to begin'

        match_with_index = re.match(pattern_with_index, statement, re.IGNORECASE)
        match_simple = re.match(pattern_simple, statement, re.IGNORECASE)

        if match_with_index:
            array_name = match_with_index.group(1)
            item_var = match_with_index.group(2)
            index_var = match_with_index.group(3)
            has_index = True
        elif match_simple:
            array_name = match_simple.group(1)
            item_var = match_simple.group(2)
            index_var = None
            has_index = False
        else:
            raise SyntaxError("use Traverse <array> with each <item> to begin: ... end traverse")

        if array_name not in self.variables:
            raise NameError(f"unknown entity {array_name}")

        array = self.variables[array_name]
        if not isinstance(array, list):
            raise TypeError(f"{array_name} is not a collection")

        body_statements = self.collect_block_from_context("end traverse")

        if not body_statements:
            raise SyntaxError("traverse body is empty")

        saved_item = self.variables.get(item_var)
        saved_index = self.variables.get(index_var) if has_index else None

        for idx, item in enumerate(array):
            self.variables[item_var] = item
            if has_index:
                self.variables[index_var] = idx

            context = ExecutionContext(source='body', body_statements=body_statements, start_index=0)
            self.context_stack.append(context)

            while context.current_index < len(context.body_statements):
                body_statement = context.body_statements[context.current_index]
                context.current_index += 1
                result = self.execute_statement(body_statement)
                if result is not None:
                    self.context_stack.pop()
                    return result

            self.context_stack.pop()

        if saved_item is not None:
            self.variables[item_var] = saved_item
        elif item_var in self.variables:
            del self.variables[item_var]

        if has_index:
            if saved_index is not None:
                self.variables[index_var] = saved_index
            elif index_var in self.variables:
                del self.variables[index_var]

    def split_collection_items(self, items_str):
        items = []
        current_tokens = []
        i = 0
        tokens = items_str.split()

        while i < len(tokens):
            token = tokens[i]
            token_lower = token.lower()

            if token_lower == "and" and i + 1 < len(tokens) and tokens[i + 1].lower() == "through":
                if current_tokens:
                    items.append(" ".join(current_tokens))
                    current_tokens = []
                i += 1
                continue
            elif token_lower == "and" and (not current_tokens or "ritual" not in " ".join(current_tokens).lower()):
                if current_tokens:
                    items.append(" ".join(current_tokens))
                    current_tokens = []
                i += 1
                continue
            else:
                current_tokens.append(token)

            i += 1

        if current_tokens:
            items.append(" ".join(current_tokens))

        return items

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

        context = ExecutionContext(source='body', body_statements=func["body"], start_index=0)
        self.context_stack.append(context)
        
        result = None
        while context.current_index < len(context.body_statements):
            body_statement = context.body_statements[context.current_index]
            context.current_index += 1
            result = self.execute_statement(body_statement)
            if result is not None:
                break

        self.context_stack.pop()

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
        if msg.startswith('whispers of "') and msg.endswith('"'):
            print(msg[len('whispers of "'):-1])
            return
        
        try:
            val = self.evaluate_expression(msg)
            if isinstance(val, list):
                print(f"[{', '.join(str(v) for v in val)}]")
            else:
                print(val)
        except:
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
        lower = statement.lower()

        if " to begin" in lower:
            pattern = r'Conjure ritual named (\w+) with (.+?) to begin'
            match = re.match(pattern, statement, re.IGNORECASE)
            if not match:
                raise SyntaxError("use Conjure ritual named <name> with <params> to begin: ... end ritual")
            name, params_str = match.groups()
            params = [p.strip() for p in params_str.split("and")]

            body_statements = self.collect_block_from_context("end ritual")

            if not body_statements:
                raise SyntaxError("ritual body is empty")

            self.functions[name] = {
                "params": params,
                "body": body_statements
            }
        else:
            pattern = r'Conjure ritual named (\w+) with (.+?) to (.+)'
            match = re.match(pattern, statement, re.IGNORECASE)
            if not match:
                raise SyntaxError("use Conjure ritual named <name> with <params> to <body>")
            name, params_str, body = match.groups()
            params = [p.strip() for p in params_str.split("and")]
            body = body.strip()
            if body.endswith('.') or body.endswith(':'):
                body = body[:-1].strip()
            self.functions[name] = {
                "params": params,
                "body": [body]
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
        
        context = ExecutionContext(source='body', body_statements=func["body"], start_index=0)
        self.context_stack.append(context)
        
        result = None
        while context.current_index < len(context.body_statements):
            body_statement = context.body_statements[context.current_index]
            context.current_index += 1
            result = self.execute_statement(body_statement)
            if result is not None:
                break
        
        self.context_stack.pop()
        
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
                    if s.endswith('.') or s.endswith(':'):
                        s = s[:-1].strip()
                    if s:
                        body_tokens.append(s)
        
        if not body_tokens:
            body_tokens = self.collect_block_from_context("end loop")
        
        if not body_tokens:
            raise SyntaxError("loop body is empty")
        
        for _ in range(count):
            context = ExecutionContext(source='body', body_statements=body_tokens, start_index=0)
            self.context_stack.append(context)
            
            while context.current_index < len(context.body_statements):
                action_statement = context.body_statements[context.current_index]
                context.current_index += 1
                result = self.execute_statement(action_statement)
                if result is not None:
                    self.context_stack.pop()
                    return result
            
            self.context_stack.pop()

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
        cond_lower = condition.lower()

        or_parts = re.split(r'\s+or\s+', cond_lower, flags=re.IGNORECASE)
        if len(or_parts) > 1:
            or_parts_orig = re.split(r'\s+or\s+', condition, flags=re.IGNORECASE)
            for part in or_parts_orig:
                if self.evaluate_condition(part.strip()):
                    return True
            return False

        and_parts = re.split(r'\s+and\s+', cond_lower, flags=re.IGNORECASE)
        if len(and_parts) > 1:
            and_parts_orig = re.split(r'\s+and\s+', condition, flags=re.IGNORECASE)
            for part in and_parts_orig:
                if not self.evaluate_condition(part.strip()):
                    return False
            return True

        if cond_lower.startswith("not "):
            inner = condition[4:].strip()
            return not self.evaluate_condition(inner)

        if " equals " in cond_lower:
            parts = re.split(r'\s+equals\s+', condition, flags=re.IGNORECASE, maxsplit=1)
            a, b = parts[0].strip(), parts[1].strip()
            return self.evaluate_expression(a) == self.evaluate_expression(b)

        if " greater than " in cond_lower:
            parts = re.split(r'\s+greater than\s+', condition, flags=re.IGNORECASE, maxsplit=1)
            a, b = parts[0].strip(), parts[1].strip()
            return self.evaluate_expression(a) > self.evaluate_expression(b)
        if " less than " in cond_lower:
            parts = re.split(r'\s+less than\s+', condition, flags=re.IGNORECASE, maxsplit=1)
            a, b = parts[0].strip(), parts[1].strip()
            return self.evaluate_expression(a) < self.evaluate_expression(b)
        
        if cond_lower == "truth":
            return True
        if cond_lower == "falsehood":
            return False
        
        if condition.strip() in self.variables:
            return bool(self.variables[condition.strip()])
        
        return False

    def evaluate_expression(self, expr):
        expr = expr.strip()
        
        if "collection holding" in expr.lower():
            pattern = r'collection holding (.+)'
            match = re.search(pattern, expr, re.IGNORECASE)
            if match:
                items_str = match.group(1).strip()
                items = self.split_collection_items(items_str)
                return [self.evaluate_expression(item.strip()) for item in items]
        
        if " bound with " in expr.lower():
            parts = re.split(r'\s+bound with\s+', expr, flags=re.IGNORECASE)
            result = ""
            for part in parts:
                val = self.evaluate_expression(part.strip())
                result += str(val)
            return result
        
        if " at position " in expr.lower():
            pattern = r'(\w+)\s+at position\s+(.+)'
            match = re.match(pattern, expr, re.IGNORECASE)
            if match:
                array_name = match.group(1).strip()
                index_expr = match.group(2).strip()

                if array_name not in self.variables:
                    raise NameError(f"unknown entity {array_name}")

                array = self.variables[array_name]
                if not isinstance(array, list):
                    raise TypeError(f"{array_name} is not a collection")

                index = self.evaluate_expression(index_expr)
                if not isinstance(index, int):
                    raise TypeError(f"index must be a number, got {type(index).__name__}")

                if index < 0 or index >= len(array):
                    raise IndexError(f"index {index} out of range for collection of length {len(array)}")

                return array[index]
        
        if expr.lower().startswith("length of "):
            array_name = expr[len("length of "):].strip()
            
            if array_name not in self.variables:
                raise NameError(f"unknown entity {array_name}")
            
            array = self.variables[array_name]
            if not isinstance(array, list):
                raise TypeError(f"{array_name} is not a collection")
            
            return len(array)
        
        if "through ritual" in expr.lower():
            pattern = r'through ritual\s+(\w+)(?:\s+with\s+(.+?))?(?=\s+and\s+through|$)'
            match = re.search(pattern, expr, re.IGNORECASE)
            if match:
                name = match.group(1)
                args = match.group(2).strip() if match.group(2) else None
                ritual_call = name
                if args:
                    ritual_call += " with " + args
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
                    raise TypeError(f"Expected number, got {type(a).__name__}: {b}")
                return a - b

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
        print("usage: python spellscript.py <filename>.spell")
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