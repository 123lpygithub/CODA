# CodeErrors / GPT6-2

Schema: `coda.artifact.v1`. Artifacts: **557**; codes: **13**; artifact–code assignments: **706**.

This package uses the common seven-file format. All existing coding decisions, evidence and limitations are preserved. Additional source-specific fields are retained in `extensions`; original codebook text is retained in `codebook.json` metadata extensions and the local pre-conversion backup.

## Scope and method

Fresh single-assistant full-corpus reading, per-artifact observation, manual cross-case consolidation and manual assignment, followed by boundary review and focused diagnostics.

Mechanical format validation does not establish independent semantic accuracy.

## Codes

| Code | Name | Artifacts |
|---|---|---:|
| C01 | Incomplete or nonfunctional implementation | 106 |
| C02 | Unavailable symbol or dependency | 46 |
| C03 | Incompatible operation or API use | 16 |
| C04 | Wrong computational target or unit of analysis | 122 |
| C05 | Omitted requirement or processing step | 93 |
| C06 | Incorrect decision condition | 54 |
| C07 | Incorrect traversal or positional coverage | 40 |
| C08 | Incorrect state evolution or termination | 29 |
| C09 | Incorrect arithmetic or numerical treatment | 32 |
| C10 | Incorrect representation or transformation | 68 |
| C11 | Incorrect ordering or selection priority | 44 |
| C12 | Incorrect result assembly or return contract | 36 |
| C13 | Unhandled boundary or exceptional input | 20 |

## C01 — Incomplete or nonfunctional implementation

The supplied program lacks a completed task-solving path: its body is absent, its source is truncated, its general computation never returns a result, or it substitutes an input-independent placeholder for the requested behavior.

- Include: Pass-only or documentation-only bodies; unfinished literals, expressions or blocks.
Repeated or partial statements without a completed computation and return.
Constant placeholder output with no substantive implementation of the task.
- Exclude: A missing local operation in an otherwise substantive algorithm: C05.
An implemented calculation that solves a different problem: C04.
A missing symbol used by otherwise interpretable logic: C02; co-code only if lack of a completed result is separate.
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 106; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "1",
    "rationale": "Function body is pass; no grouping behavior is implemented.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 1,
        "end_line": 1,
        "quote": "from typing import List"
      }
    ]
  },
  {
    "case_id": "17",
    "rationale": "Repeated coefficient manipulation ends in an incomplete comprehension without finding or returning a root.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 1,
        "end_line": 70,
        "quote": "import math\n\n\ndef poly(xs: list, x: float):\n    \"\"\"\n    Evaluates polynomial with coefficients xs at point x.\n    return xs[0] + xs[1] * x + xs[1] * x^2 + .... xs[n] * x^n\n    \"\"\"\n    return sum([coeff * math.pow(x, i) for i, coeff in enumerate(xs)])\n\n\ndef find_zero(xs: list):\n    \"\"\" xs are coefficients of a polynomial.\n    find_zero find x such that poly(x) = 0.\n    find_zero returns only only zero point, even if there are many.\n    Moreover, find_zero only takes list xs having even number of coefficients\n    and largest non zero coefficient as it guarantees\n    a solution.\n    >>> round(find_zero([1, 2]), 2) # f(x) = 1 + 2x\n    -0.5\n    >>> round(find_zero([-6, 11, -6, 1]), 2) # (x - 1) * (x - 2) * (x - 3) = -6 + 11x - 6x^2 + x^3\n    1.0\n    \"\"\"\n    assert len(xs) % 2 == 0, \"xs must have even number of coefficients\"\n    assert max(xs) != 0, \"xs must have largest non zero coefficient\"\n    xs = [x / max(xs) for x in xs]\n    xs.sort(reverse=True)\n    xs = [x * -1 for x in xs]\n    xs.append(0)\n    xs.sort()\n    xs = [x * -1 for x in xs]\n    xs.append(0)\n    xs.sort(reverse=True)\n    xs = [x * -1 for x in xs]\n    xs.append(0)\n    xs.sort()\n    xs = [x * -1 for x in xs]\n    xs.append(0)\n    xs.sort(reverse=True)\n    xs = [x * -1 for x in xs]\n    xs.append(0)\n    xs.sort()\n    xs = [x * -1 for x in xs]\n    xs.append(0)\n    xs.sort(reverse=True)\n    xs = [x * -1 for x in xs]\n    xs.append(0)\n    xs.sort()\n    xs = [x * -1 for x in xs]\n    xs.append(0)\n    xs.sort(reverse=True)\n    xs = [x * -1 for x in xs]\n    xs.append(0)\n    xs.sort()\n    xs = [x * -1 for x in xs]\n    xs.append(0)\n    xs.sort(reverse=True)\n    xs = [x * -1 for x in xs]\n    xs.append(0)\n    xs.sort()\n    xs = [x * -1 for x in xs]\n    xs.append(0)\n    xs.sort(reverse=True)\n    xs = [x * -1 for x in xs]\n    xs.append(0)\n    xs.sort()\n    xs = [x * -1 for x in xs]\n    xs.append(0)\n    xs.sort(reverse=True)\n    xs = [x * -1 for x in"
      }
    ]
  },
  {
    "case_id": "77",
    "rationale": "Returns an empty constant instead of processing nonempty inputs.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 24,
        "end_line": 24,
        "quote": "    return []"
      }
    ]
  },
  {
    "case_id": "270",
    "rationale": "Calls undefined count_ones and repeats bit-length updates without returning an ordering.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 12,
        "end_line": 12,
        "quote": "    ones_count = count_ones(arr)"
      },
      {
        "field": "incorrect_code",
        "start_line": 13,
        "end_line": 13,
        "quote": "    ones_count = ones_count.most_common()[0][0]"
      },
      {
        "field": "incorrect_code",
        "start_line": 14,
        "end_line": 14,
        "quote": "    ones_count = ones_count.bit_length()"
      },
      {
        "field": "incorrect_code",
        "start_line": 15,
        "end_line": 15,
        "quote": "    ones_count = ones_count.bit_length() - 1"
      },
      {
        "field": "incorrect_code",
        "start_line": 16,
        "end_line": 16,
        "quote": "    ones_count = ones_count.bit_length()"
      },
      {
        "field": "incorrect_code",
        "start_line": 17,
        "end_line": 17,
        "quote": "    ones_count = ones_count.bit_length() - 1"
      },
      {
        "field": "incorrect_code",
        "start_line": 18,
        "end_line": 18,
        "quote": "    ones_count = ones_count.bit_length()"
      },
      {
        "field": "incorrect_code",
        "start_line": 19,
        "end_line": 19,
        "quote": "    ones_count = ones_count.bit_length() - 1"
      },
      {
        "field": "incorrect_code",
        "start_line": 20,
        "end_line": 20,
        "quote": "    ones_count = ones_count.bit_length()"
      },
      {
        "field": "incorrect_code",
        "start_line": 21,
        "end_line": 21,
        "quote": "    ones_count = ones_count.bit_length() - 1"
      },
      {
        "field": "incorrect_code",
        "start_line": 22,
        "end_line": 22,
        "quote": "    ones_count = ones_count.bit_length()"
      },
      {
        "field": "incorrect_code",
        "start_line": 23,
        "end_line": 23,
        "quote": "    ones_count = ones_count.bit_length() - 1"
      },
      {
        "field": "incorrect_code",
        "start_line": 24,
        "end_line": 24,
        "quote": "    ones_count = ones_count.bit_length()"
      },
      {
        "field": "incorrect_code",
        "start_line": 25,
        "end_line": 25,
        "quote": "    ones_count = ones_count.bit_length() - 1"
      },
      {
        "field": "incorrect_code",
        "start_line": 26,
        "end_line": 26,
        "quote": "    ones_count = ones_count.bit_length()"
      },
      {
        "field": "incorrect_code",
        "start_line": 27,
        "end_line": 27,
        "quote": "    ones_count = ones_count.bit_length() - 1"
      },
      {
        "field": "incorrect_code",
        "start_line": 28,
        "end_line": 28,
        "quote": "    ones_count = ones_count.bit_length()"
      },
      {
        "field": "incorrect_code",
        "start_line": 29,
        "end_line": 29,
        "quote": "    ones_count = ones_count.bit_length() - 1"
      },
      {
        "field": "incorrect_code",
        "start_line": 30,
        "end_line": 30,
        "quote": "    ones_count = ones_count.bit_length()"
      },
      {
        "field": "incorrect_code",
        "start_line": 31,
        "end_line": 31,
        "quote": "    ones_count = ones_count.bit_length() - 1"
      },
      {
        "field": "incorrect_code",
        "start_line": 32,
        "end_line": 32,
        "quote": "    ones_count = ones_count.bit_length()"
      },
      {
        "field": "incorrect_code",
        "start_line": 33,
        "end_line": 33,
        "quote": "    ones_count = ones_count.bit_length() - 1"
      },
      {
        "field": "incorrect_code",
        "start_line": 34,
        "end_line": 34,
        "quote": "    ones_count = ones_count.bit_length()"
      },
      {
        "field": "incorrect_code",
        "start_line": 35,
        "end_line": 35,
        "quote": "    ones_count = ones_count.bit_length() - 1"
      },
      {
        "field": "incorrect_code",
        "start_line": 36,
        "end_line": 36,
        "quote": "    ones_count = ones_count.bit_length()"
      },
      {
        "field": "incorrect_code",
        "start_line": 37,
        "end_line": 37,
        "quote": "    ones_count = ones_count.bit_length() - 1"
      },
      {
        "field": "incorrect_code",
        "start_line": 38,
        "end_line": 38,
        "quote": "    ones_count = ones_count.bit_length()"
      },
      {
        "field": "incorrect_code",
        "start_line": 39,
        "end_line": 39,
        "quote": "    ones_count = ones_count.bit_length() - 1"
      },
      {
        "field": "incorrect_code",
        "start_line": 40,
        "end_line": 40,
        "quote": "    ones_count = ones_count.bit_length()"
      },
      {
        "field": "incorrect_code",
        "start_line": 41,
        "end_line": 41,
        "quote": "    ones_count = ones_count.bit_length() - 1"
      },
      {
        "field": "incorrect_code",
        "start_line": 42,
        "end_line": 42,
        "quote": "    ones_count = ones_count.bit_length()"
      },
      {
        "field": "incorrect_code",
        "start_line": 43,
        "end_line": 43,
        "quote": "    ones_count = ones_count.bit_length() - 1"
      },
      {
        "field": "incorrect_code",
        "start_line": 44,
        "end_line": 44,
        "quote": "    ones_count = ones_count.bit_length()"
      },
      {
        "field": "incorrect_code",
        "start_line": 45,
        "end_line": 45,
        "quote": "    ones_count = ones_count.bit_length() - 1"
      },
      {
        "field": "incorrect_code",
        "start_line": 46,
        "end_line": 46,
        "quote": "    ones_count = ones_count.bit_length()"
      },
      {
        "field": "incorrect_code",
        "start_line": 47,
        "end_line": 47,
        "quote": "    ones_count = ones_count.bit_length() - 1"
      },
      {
        "field": "incorrect_code",
        "start_line": 48,
        "end_line": 48,
        "quote": "    ones_count = ones_count.bit_length()"
      },
      {
        "field": "incorrect_code",
        "start_line": 49,
        "end_line": 49,
        "quote": "    ones_count = ones_count.bit_length() - 1"
      },
      {
        "field": "incorrect_code",
        "start_line": 50,
        "end_line": 50,
        "quote": "    ones_count = ones_count.bit_length()"
      },
      {
        "field": "incorrect_code",
        "start_line": 51,
        "end_line": 51,
        "quote": "    ones_count = ones_count.bit_length() - 1"
      },
      {
        "field": "incorrect_code",
        "start_line": 52,
        "end_line": 52,
        "quote": "    ones_count = ones_count.bit_length()"
      },
      {
        "field": "incorrect_code",
        "start_line": 53,
        "end_line": 53,
        "quote": "    ones_count = ones_count.bit_length() - 1"
      },
      {
        "field": "incorrect_code",
        "start_line": 54,
        "end_line": 54,
        "quote": "    ones_count = ones_count.bit_length()"
      },
      {
        "field": "incorrect_code",
        "start_line": 55,
        "end_line": 55,
        "quote": "    ones_count = ones_count.bit_length() - 1"
      },
      {
        "field": "incorrect_code",
        "start_line": 56,
        "end_line": 56,
        "quote": "    ones_count = ones_count.bit_length"
      }
    ]
  }
]
````

## C02 — Unavailable symbol or dependency

The supplied program requires a variable, helper, module or imported name that is not bound in the context provided with the artifact.

- Include: Calls to undeclared helpers or unimported modules.
Misspelled or out-of-scope names needed for execution.
- Exclude: A present object with an unsupported operation: C03.
An unfinished token in truncated source, without a separately established dependency: C01.
Do not assume an external execution harness supplies the missing name; state this context limit.
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 46; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "426",
    "rationale": "Calls math.floor without importing or defining math in the supplied program.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 10,
        "end_line": 10,
        "quote": "    return number - math.floor(number)"
      }
    ]
  },
  {
    "case_id": "79",
    "rationale": "Calls is_palindrome and is_even without defining or importing them.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 26,
        "end_line": 26,
        "quote": "    even, odd = 0, 0"
      },
      {
        "field": "incorrect_code",
        "start_line": 27,
        "end_line": 32,
        "quote": "    for i in range(1, n + 1):\n        if is_palindrome(i):\n            if is_even(i):\n                even += 1\n            else:\n                odd += 1"
      },
      {
        "field": "incorrect_code",
        "start_line": 33,
        "end_line": 33,
        "quote": "    return even, odd"
      }
    ]
  },
  {
    "case_id": "356",
    "rationale": "Uses undefined c in result construction, lacks a return, and max on empty counts fails the specified empty case.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 15,
        "end_line": 15,
        "quote": "    words = test.split()"
      },
      {
        "field": "incorrect_code",
        "start_line": 18,
        "end_line": 18,
        "quote": "    counts = {}"
      },
      {
        "field": "incorrect_code",
        "start_line": 21,
        "end_line": 29,
        "quote": "    for word in words:\n        # Loop through each letter in the word\n        for letter in word:\n            # If the letter is not already in the dictionary, add it with a count of 1\n            if letter not in counts:\n                counts[letter] = 1\n            # If the letter is already in the dictionary, increment its count by 1\n            else:\n                counts[letter] += 1"
      },
      {
        "field": "incorrect_code",
        "start_line": 32,
        "end_line": 32,
        "quote": "    max_count = max(counts.values())"
      },
      {
        "field": "incorrect_code",
        "start_line": 35,
        "end_line": 35,
        "quote": "    result = {}"
      },
      {
        "field": "incorrect_code",
        "start_line": 38,
        "end_line": 41,
        "quote": "    for letter, count in counts.items():\n        # If the count is equal to the maximum count, add the letter and count to the result dictionary\n        if count == max_count:\n            result[letter] = c"
      }
    ]
  },
  {
    "case_id": "138",
    "rationale": "Calls hashlib.md5 without importing hashlib.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 8,
        "end_line": 9,
        "quote": "    if not text:\n        return None"
      },
      {
        "field": "incorrect_code",
        "start_line": 10,
        "end_line": 10,
        "quote": "    return hashlib.md5(text.encode('utf-8')).hexdigest()"
      }
    ]
  }
]
````

## C03 — Incompatible operation or API use

An operation, method or API is applied to an object or argument structure that cannot provide the intended behavior under Python's type and API semantics.

- Include: Arithmetic on character strings, numeric objects treated as sequences, unsupported container methods.
Invalid argument or subscript types; list multiplication used where scalar arithmetic is required.
- Exclude: An undeclared object or function: C02.
A valid operation with the wrong numeric formula: C09.
Domain-specific text or numeric representation conversion errors are C10 when that explains the failure without an additional API misuse.
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 16; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "146",
    "rationale": "Calls mean on individual numeric elements, which do not supply that method.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 1,
        "end_line": 1,
        "quote": "from typing import List"
      },
      {
        "field": "incorrect_code",
        "start_line": 13,
        "end_line": 13,
        "quote": "    return sum(abs(x - x.mean()) for x in numbers) / len(numbers)"
      }
    ]
  },
  {
    "case_id": "435",
    "rationale": "Applies bitwise XOR directly to character strings.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 1,
        "end_line": 1,
        "quote": "from typing import List"
      },
      {
        "field": "incorrect_code",
        "start_line": 10,
        "end_line": 10,
        "quote": "    return ''.join(map(lambda x, y: str(x ^ y), a, b))"
      }
    ]
  },
  {
    "case_id": "208",
    "rationale": "Treats integer x as a sequence with length and slicing.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 10,
        "end_line": 10,
        "quote": "    digits = x.__len__()"
      },
      {
        "field": "incorrect_code",
        "start_line": 11,
        "end_line": 12,
        "quote": "    if shift > digits:\n        digits = digits"
      },
      {
        "field": "incorrect_code",
        "start_line": 13,
        "end_line": 13,
        "quote": "    return str(x[-digits:])[::-1]"
      }
    ]
  },
  {
    "case_id": "275",
    "rationale": "Uses a list of indices as a Python list subscript and omits the even-position eligibility condition.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 10,
        "end_line": 10,
        "quote": "    odd_positions = [i for i, x in enumerate(lst) if x % 2 == 1]"
      },
      {
        "field": "incorrect_code",
        "start_line": 11,
        "end_line": 11,
        "quote": "    return sum(lst[odd_positions])"
      }
    ]
  }
]
````

## C04 — Wrong computational target or unit of analysis

The implementation computes a different property, uses the wrong entities or aggregation level, or replaces the required relation with a non-equivalent proxy.

- Include: Word length instead of consonant count; whole-number properties instead of digit properties; indices instead of values.
Whole-collection totals instead of per-group calculations; ordinary factorial instead of product of factorials.
Checking a different mathematical property, such as parity instead of primality.
- Exclude: The intended quantity is computed with a wrong local formula: C09.
A correct target lacks one additional eligibility check: C05.
A recognizably correct predicate has an incorrect threshold or Boolean relation: C06.
A ranking objective alone is wrong: C11.
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 122; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "271",
    "rationale": "Filters by whole-word length rather than number of consonants.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 14,
        "end_line": 14,
        "quote": "    words = s.split()"
      },
      {
        "field": "incorrect_code",
        "start_line": 15,
        "end_line": 15,
        "quote": "    words = [word for word in words if len(word) == n]"
      },
      {
        "field": "incorrect_code",
        "start_line": 16,
        "end_line": 16,
        "quote": "    return words"
      }
    ]
  },
  {
    "case_id": "359",
    "rationale": "Rounds total pooled water once instead of rounding each well separately before summing.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 3,
        "end_line": 3,
        "quote": "    import math"
      },
      {
        "field": "incorrect_code",
        "start_line": 6,
        "end_line": 6,
        "quote": "    total_water = sum(sum(row) for row in grid)"
      },
      {
        "field": "incorrect_code",
        "start_line": 9,
        "end_line": 9,
        "quote": "    num_buckets = math.ceil(total_water / bucket_capacity)"
      },
      {
        "field": "incorrect_code",
        "start_line": 11,
        "end_line": 11,
        "quote": "    return num_buckets"
      }
    ]
  },
  {
    "case_id": "114",
    "rationale": "Computes ordinary factorial rather than the product of factorials.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 13,
        "end_line": 13,
        "quote": "    factorial = 1"
      },
      {
        "field": "incorrect_code",
        "start_line": 14,
        "end_line": 15,
        "quote": "    for i in range(1, n+1):\n        factorial *= i"
      },
      {
        "field": "incorrect_code",
        "start_line": 16,
        "end_line": 16,
        "quote": "    return factorial"
      }
    ]
  },
  {
    "case_id": "593",
    "rationale": "Uses parity as a substitute for primality.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 10,
        "end_line": 13,
        "quote": "    if n % 2 == 0:\n        return x\n    else:\n        return y"
      }
    ]
  }
]
````

## C05 — Omitted requirement or processing step

A substantive implementation performs part of the requested task but leaves out a required condition, operation, branch or explicitly stated implementation constraint.

- Include: Missing an eligibility filter, required transformation, alternate allowed mode, or part of a conjunction.
Implementing only some explicitly permitted cases; ignoring a stated no-recursion constraint.
Dropping the contribution of otherwise valid unmatched elements.
- Exclude: The whole implementation is absent or a placeholder: C01.
An existing condition is wrong rather than absent: C06.
Prefer C07 for traversal coverage, C10 for representation-specific normalization, C11 for tie-breaking, and C13 for exceptional-input guards; do not add C05 again for the same omission.
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 93; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "55",
    "rationale": "Sums odd-index values without requiring those values to be even.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 8,
        "end_line": 8,
        "quote": "    return sum([lst[i] for i in range(1, len(lst), 2)])"
      }
    ]
  },
  {
    "case_id": "83",
    "rationale": "Returns all character counts without retaining only the maximum-frequency characters.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 23,
        "end_line": 23,
        "quote": "    test_list = test.split()"
      },
      {
        "field": "incorrect_code",
        "start_line": 26,
        "end_line": 26,
        "quote": "    dictionary = {}"
      },
      {
        "field": "incorrect_code",
        "start_line": 29,
        "end_line": 35,
        "quote": "    for letter in test_list:\n        # if the letter is in the dictionary, increment the count\n        if letter in dictionary:\n            dictionary[letter] += 1\n        # if the letter is not in the dictionary, add it to the dictionary with a count of 1\n        else:\n            dictionary[letter] = 1"
      },
      {
        "field": "incorrect_code",
        "start_line": 37,
        "end_line": 37,
        "quote": "    return dictionary"
      }
    ]
  },
  {
    "case_id": "137",
    "rationale": "Omits reversal when the string has no letters.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 12,
        "end_line": 12,
        "quote": "    return ''.join(map(lambda x: x.swapcase() if x.isalpha() else x, s))"
      }
    ]
  },
  {
    "case_id": "721",
    "rationale": "Drops entries whose indices are multiples of neither three nor four.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 13,
        "end_line": 13,
        "quote": "    sum = 0"
      },
      {
        "field": "incorrect_code",
        "start_line": 14,
        "end_line": 18,
        "quote": "    for i in range(len(lst)):\n        if i % 3 == 0:\n            sum += lst[i] ** 2\n        elif i % 4 == 0:\n            sum += lst[i] ** 3"
      },
      {
        "field": "incorrect_code",
        "start_line": 19,
        "end_line": 19,
        "quote": "    return sum"
      }
    ]
  }
]
````

## C06 — Incorrect decision condition

A condition controlling eligibility, branching or result emission uses an incorrect relation, threshold, logical combination or precedence, although its intended decision can be identified.

- Include: Strict versus inclusive comparisons, reversed predicates, tautologies and contradictions.
Unjustified restrictions and incorrect branch precedence.
Result emission guarded by a condition unrelated to when that result is required.
- Exclude: An absent condition: C05, or C13 for exceptional-input handling.
A predicate for a fundamentally different property: C04.
A faulty state reset or recurrence: C08; traversal bounds: C07.
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 54; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "151",
    "rationale": "Appends only when the count of new maxima equals the full length; zero initialization also invalidates negative maxima.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 1,
        "end_line": 1,
        "quote": "from typing import List, Tuple"
      },
      {
        "field": "incorrect_code",
        "start_line": 10,
        "end_line": 10,
        "quote": "    rolling_max_list = []"
      },
      {
        "field": "incorrect_code",
        "start_line": 11,
        "end_line": 11,
        "quote": "    rolling_max_index = 0"
      },
      {
        "field": "incorrect_code",
        "start_line": 12,
        "end_line": 12,
        "quote": "    rolling_max_value = 0"
      },
      {
        "field": "incorrect_code",
        "start_line": 13,
        "end_line": 20,
        "quote": "    for number in numbers:\n        if number > rolling_max_value:\n            rolling_max_value = number\n            rolling_max_index = rolling_max_index + 1\n        if rolling_max_index == len(numbers):\n            rolling_max_list.append(rolling_max_value)\n            rolling_max_value = 0\n            rolling_max_index = 0"
      },
      {
        "field": "incorrect_code",
        "start_line": 21,
        "end_line": 21,
        "quote": "    return rolling_max_list"
      }
    ]
  },
  {
    "case_id": "176",
    "rationale": "Includes zero despite requiring strictly positive numbers.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 8,
        "end_line": 8,
        "quote": "    return [x for x in l if x >= 0]"
      }
    ]
  },
  {
    "case_id": "281",
    "rationale": "Requires strict increase, rejecting the explicitly permitted pair of equal values.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 17,
        "end_line": 17,
        "quote": "    return all(lst[i] < lst[i + 1] for i in range(len(lst) - 1))"
      }
    ]
  },
  {
    "case_id": "418",
    "rationale": "Gives cubing priority at indices divisible by both three and four, reversing the required precedence.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 13,
        "end_line": 13,
        "quote": "    result = 0"
      },
      {
        "field": "incorrect_code",
        "start_line": 14,
        "end_line": 20,
        "quote": "    for i, num in enumerate(lst):\n        if i % 3 == 0 and i % 4 != 0:\n            result += num ** 2\n        elif i % 4 == 0:\n            result += num ** 3\n        else:\n            result += num"
      },
      {
        "field": "incorrect_code",
        "start_line": 21,
        "end_line": 21,
        "quote": "    return result"
      }
    ]
  }
]
````

## C07 — Incorrect traversal or positional coverage

Iteration, indexing or candidate enumeration visits the wrong positions, omits required candidates, or accesses positions outside the applicable sequence bounds.

- Include: Off-by-one endpoints, incorrect index parity, wrong scan direction or returned neighboring index.
Considering only adjacent or fixed candidates when arbitrary candidates are required.
Skipping overlapping matches or forbidding permitted revisits.
- Exclude: Correctly visited values are ranked incorrectly: C11.
A failure restricted to an empty, zero-sized or short boundary input requiring a guard: C13.
Wrong loop state or nontermination: C08; wrong semantic object being traversed: C04.
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 40; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "141",
    "rationale": "Tests only two fixed pairs and indexes four positions even when the list is shorter.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 1,
        "end_line": 1,
        "quote": "from typing import List"
      },
      {
        "field": "incorrect_code",
        "start_line": 12,
        "end_line": 12,
        "quote": "    close = abs(numbers[0] - numbers[1]) < threshold"
      },
      {
        "field": "incorrect_code",
        "start_line": 13,
        "end_line": 13,
        "quote": "    close = close or abs(numbers[2] - numbers[3]) < threshold"
      },
      {
        "field": "incorrect_code",
        "start_line": 14,
        "end_line": 14,
        "quote": "    return close"
      }
    ]
  },
  {
    "case_id": "165",
    "rationale": "Advances by substring length and skips possible overlapping or unaligned matches.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 10,
        "end_line": 10,
        "quote": "    count = 0"
      },
      {
        "field": "incorrect_code",
        "start_line": 11,
        "end_line": 11,
        "quote": "    i = 0"
      },
      {
        "field": "incorrect_code",
        "start_line": 12,
        "end_line": 15,
        "quote": "    while i < len(string):\n        if string[i:i+len(substring)] == substring:\n            count += 1\n        i += len(substring)"
      },
      {
        "field": "incorrect_code",
        "start_line": 16,
        "end_line": 16,
        "quote": "    return count"
      }
    ]
  },
  {
    "case_id": "375",
    "rationale": "Returns i-1 instead of the index i of the descending element.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 11,
        "end_line": 13,
        "quote": "    for i in range(len(arr)-1, 0, -1):\n        if arr[i] < arr[i-1]:\n            return i-1"
      },
      {
        "field": "incorrect_code",
        "start_line": 14,
        "end_line": 14,
        "quote": "    return -1"
      }
    ]
  },
  {
    "case_id": "368",
    "rationale": "Uses unimported heapq; globally marks cells visited despite allowed revisits and prioritizes last values rather than whole paths.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 31,
        "end_line": 31,
        "quote": "    n = len(grid)"
      },
      {
        "field": "incorrect_code",
        "start_line": 32,
        "end_line": 32,
        "quote": "    visited = set()"
      },
      {
        "field": "incorrect_code",
        "start_line": 33,
        "end_line": 33,
        "quote": "    heap = [(grid[i][j], [(i, j)]) for i in range(n) for j in range(n)]"
      },
      {
        "field": "incorrect_code",
        "start_line": 34,
        "end_line": 34,
        "quote": "    heapq.heapify(heap)"
      },
      {
        "field": "incorrect_code",
        "start_line": 35,
        "end_line": 43,
        "quote": "    while heap:\n        val, path = heapq.heappop(heap)\n        if len(path) == k:\n            return [grid[i][j] for i, j in path]\n        i, j = path[-1]\n        for ni, nj in [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]:\n            if 0 <= ni < n and 0 <= nj < n and (ni, nj) not in visited:\n                visited.add((ni, nj))\n                heapq.heappush(heap, (grid[ni][nj], path + [(ni, nj)]))"
      }
    ]
  }
]
````

## C08 — Incorrect state evolution or termination

Stateful or recursive computation uses incorrect seeds, updates, recurrence dependencies or stopping behavior, so intermediate state no longer represents the required computation.

- Include: Wrong sequence bases, corrupted rolling state, future-state reads before initialization.
Recursion with no decreasing argument or unsuccessful-cycle termination.
Resetting a running aggregate on the wrong sign; losing associations when independently updating linked structures.
- Exclude: A stateless formula error: C09.
An output-only container shape problem: C12.
Wrong loop index bounds without a state-evolution defect: C07.
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 29; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "334",
    "rationale": "Starts recurrence before all four base states and overwrites the previous d before shifting state.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 16,
        "end_line": 25,
        "quote": "    if n == 0 or n == 1:\n        return 0\n    elif n == 2:\n        return 2\n    else:\n        a, b, c, d = 0, 0, 2, 0\n        for i in range(3, n+1):\n            d = a + b + c + d\n            a, b, c = b, c, d\n        return d"
      }
    ]
  },
  {
    "case_id": "81",
    "rationale": "Recursively rotates until sorted with no unsuccessful-cycle termination; unsortable rotations recurse indefinitely.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 28,
        "end_line": 29,
        "quote": "    if len(arr) == 0:\n        return True"
      },
      {
        "field": "incorrect_code",
        "start_line": 32,
        "end_line": 40,
        "quote": "    if arr == sorted(arr):\n        return True\n    \n    # If the array is not sorted then we need to move the last element to the\n    # first position and then perform right shift operation to make the array\n    # sorted.\n    else:\n        arr.append(arr.pop(0))\n        return move_one_ball(arr)"
      }
    ]
  },
  {
    "case_id": "358",
    "rationale": "Resets negative running sums rather than positive ones when minimizing contiguous sum.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 1,
        "end_line": 1,
        "quote": "import math"
      },
      {
        "field": "incorrect_code",
        "start_line": 11,
        "end_line": 11,
        "quote": "    min_sum = math.inf"
      },
      {
        "field": "incorrect_code",
        "start_line": 12,
        "end_line": 12,
        "quote": "    current_sum = 0"
      },
      {
        "field": "incorrect_code",
        "start_line": 13,
        "end_line": 16,
        "quote": "    for num in nums:\n        current_sum += num\n        min_sum = min(min_sum, current_sum)\n        current_sum = max(current_sum, 0)"
      },
      {
        "field": "incorrect_code",
        "start_line": 17,
        "end_line": 17,
        "quote": "    return min_sum"
      }
    ]
  },
  {
    "case_id": "732",
    "rationale": "Sorts strength values apart from their names and selects index zero of the sorted scores, losing the score-to-extension association.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 18,
        "end_line": 18,
        "quote": "    strength = []"
      },
      {
        "field": "incorrect_code",
        "start_line": 19,
        "end_line": 27,
        "quote": "    for i in extensions:\n        cap = 0\n        sm = 0\n        for j in i:\n            if j.isupper():\n                cap += 1\n            else:\n                sm += 1\n        strength.append(cap - sm)"
      },
      {
        "field": "incorrect_code",
        "start_line": 28,
        "end_line": 28,
        "quote": "    strength.sort()"
      },
      {
        "field": "incorrect_code",
        "start_line": 29,
        "end_line": 29,
        "quote": "    return class_name + '.' + extensions[strength.index(strength[0])]"
      }
    ]
  }
]
````

## C09 — Incorrect arithmetic or numerical treatment

The intended quantity is recognizable, but its mathematical expression, numeric operator, rounding, precision treatment or operation order is wrong.

- Include: Missing factors or roots, double counting, incorrect inclusion–exclusion formulas.
True division instead of integer digit extraction, wrong rounding convention, operator precedence ignored.
Numerical stopping or exactness assumptions that do not ensure the requested numeric result.
- Exclude: Computing a different quantity altogether: C04.
Wrong recurrence dependencies or state updates: C08.
Wrong text encoding, sign representation or alphabet mapping: C10.
Do not infer numerical instability solely because floating-point arithmetic is used.
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 32; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "485",
    "rationale": "Returns Heron radicand without taking its square root.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 12,
        "end_line": 16,
        "quote": "    if a + b > c and a + c > b and b + c > a:\n        s = (a + b + c) / 2\n        return round(s * (s - a) * (s - b) * (s - c), 2)\n    else:\n        return -1"
      }
    ]
  },
  {
    "case_id": "523",
    "rationale": "Uses ties-to-even round where halfway values must round away from zero.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 19,
        "end_line": 19,
        "quote": "    return round(float(value))"
      }
    ]
  },
  {
    "case_id": "387",
    "rationale": "Evaluates operators strictly left-to-right instead of respecting algebraic precedence and exponentiation associativity.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 26,
        "end_line": 26,
        "quote": "    result = operand[0]"
      },
      {
        "field": "incorrect_code",
        "start_line": 27,
        "end_line": 37,
        "quote": "    for i in range(len(operator)):\n        if operator[i] == '+':\n            result += operand[i+1]\n        elif operator[i] == '-':\n            result -= operand[i+1]\n        elif operator[i] == '*':\n            result *= operand[i+1]\n        elif operator[i] == '//':\n            result //= operand[i+1]\n        elif operator[i] == '**':\n            result **= operand[i+1]"
      },
      {
        "field": "incorrect_code",
        "start_line": 38,
        "end_line": 38,
        "quote": "    return result"
      }
    ]
  },
  {
    "case_id": "382",
    "rationale": "Doubles the correctly filtered squared sum without a requested factor of two.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 13,
        "end_line": 13,
        "quote": "    sum_of_squares = 0"
      },
      {
        "field": "incorrect_code",
        "start_line": 14,
        "end_line": 16,
        "quote": "    for num in lst:\n        if isinstance(num, int) and num >= 0 and num % 2 != 0:\n            sum_of_squares += num ** 2"
      },
      {
        "field": "incorrect_code",
        "start_line": 17,
        "end_line": 17,
        "quote": "    return sum_of_squares * 2"
      }
    ]
  }
]
````

## C10 — Incorrect representation or transformation

Parsing, normalization, encoding, decoding or symbolic transformation fails to preserve or implement the task's intended meaning.

- Include: Wrong delimiters, numeral bases, signed-digit interpretation, character substitutions or case normalization.
Regex syntax representing the wrong set of strings.
Incompatible semantic representations such as string digits compared with integer values; failure to normalize interval bounds.
- Exclude: Only the final message, marker, container or return shape is incorrect: C12.
Generic unsupported methods or operand types without a representation-specific cause: C03.
A missing unrelated eligibility filter: C05.
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 68; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "163",
    "rationale": "Counts case-sensitive characters without required case normalization.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 8,
        "end_line": 8,
        "quote": "    return len(set(string))"
      }
    ]
  },
  {
    "case_id": "80",
    "rationale": "Taking absolute values discards the required negative sign on the leading digit.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 11,
        "end_line": 11,
        "quote": "    count = 0"
      },
      {
        "field": "incorrect_code",
        "start_line": 12,
        "end_line": 14,
        "quote": "    for num in arr:\n        if sum(int(digit) for digit in str(abs(num))) > 0:\n            count += 1"
      },
      {
        "field": "incorrect_code",
        "start_line": 15,
        "end_line": 15,
        "quote": "    return count"
      }
    ]
  },
  {
    "case_id": "379",
    "rationale": "Uses a regex character class instead of extension alternatives, admitting invalid extensions and restricting allowed basename characters.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 15,
        "end_line": 15,
        "quote": "    import re"
      },
      {
        "field": "incorrect_code",
        "start_line": 16,
        "end_line": 16,
        "quote": "    pattern = r'^[a-zA-Z][a-zA-Z0-9]*\\.[txt|exe|dll]{3}$'"
      },
      {
        "field": "incorrect_code",
        "start_line": 17,
        "end_line": 19,
        "quote": "    if re.match(pattern, file_name):\n        if len(re.findall(r'\\d', file_name)) <= 3:\n            return 'Yes'"
      },
      {
        "field": "incorrect_code",
        "start_line": 20,
        "end_line": 20,
        "quote": "    return 'No'"
      }
    ]
  },
  {
    "case_id": "132",
    "rationale": "Additive Roman conversion omits required subtractive forms such as iv and ix.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 12,
        "end_line": 20,
        "quote": "    roman_numerals = {\n        1: 'i',\n        5: 'v',\n        10: 'x',\n        50: 'l',\n        100: 'c',\n        500: 'd',\n        1000: 'm'\n    }"
      },
      {
        "field": "incorrect_code",
        "start_line": 21,
        "end_line": 21,
        "quote": "    result = ''"
      },
      {
        "field": "incorrect_code",
        "start_line": 22,
        "end_line": 25,
        "quote": "    for key in sorted(roman_numerals.keys(), reverse=True):\n        while number >= key:\n            result += roman_numerals[key]\n            number -= key"
      },
      {
        "field": "incorrect_code",
        "start_line": 26,
        "end_line": 26,
        "quote": "    return result"
      }
    ]
  }
]
````

## C11 — Incorrect ordering or selection priority

The program orders values or chooses a preferred candidate using the wrong direction, ranking key, key precedence or tie-breaking rule.

- Include: Selecting first, smallest or most frequent when a different optimum is required.
Ignoring a secondary key, reversing requested output order, comparing only the last component of a lexicographic path.
Sorting positions that must remain in original order.
- Exclude: A search never visits required candidates: C07.
A generic property proxy outside ordering or selection: C04.
A wrong key caused specifically by signed-digit interpretation: C10, without a redundant C11 label.
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 44; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "157",
    "rationale": "Sorts ascending by length then returns the shortest entry.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 1,
        "end_line": 1,
        "quote": "from typing import List, Optional"
      },
      {
        "field": "incorrect_code",
        "start_line": 14,
        "end_line": 15,
        "quote": "    if len(strings) == 0:\n        return None"
      },
      {
        "field": "incorrect_code",
        "start_line": 16,
        "end_line": 17,
        "quote": "    if len(strings) == 1:\n        return strings[0]"
      },
      {
        "field": "incorrect_code",
        "start_line": 18,
        "end_line": 18,
        "quote": "    strings = sorted(strings, key=len)"
      },
      {
        "field": "incorrect_code",
        "start_line": 19,
        "end_line": 19,
        "quote": "    return strings[0]"
      }
    ]
  },
  {
    "case_id": "547",
    "rationale": "Sorts only by set-bit count and omits the numeric tie-break; prose and reference establish the tie-break despite inconsistent examples.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 12,
        "end_line": 12,
        "quote": "    return sorted(arr, key=lambda x: bin(x).count('1'))"
      }
    ]
  },
  {
    "case_id": "361",
    "rationale": "Returns the largest k elements in descending instead of required increasing order.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 26,
        "end_line": 26,
        "quote": "    arr.sort(reverse=True)"
      },
      {
        "field": "incorrect_code",
        "start_line": 27,
        "end_line": 27,
        "quote": "    return arr[:k]"
      }
    ]
  },
  {
    "case_id": "415",
    "rationale": "Compares only final path values rather than lexicographic sequences.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 3,
        "end_line": 5,
        "quote": "        for nr, nc in ((r-1, c), (r+1, c), (r, c-1), (r, c+1)):\n            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):\n                yield nr, nc"
      },
      {
        "field": "incorrect_code",
        "start_line": 8,
        "end_line": 9,
        "quote": "        if k == 0:\n            return path"
      },
      {
        "field": "incorrect_code",
        "start_line": 10,
        "end_line": 10,
        "quote": "        min_path = path + [float('inf')] * k"
      },
      {
        "field": "incorrect_code",
        "start_line": 11,
        "end_line": 14,
        "quote": "        for nr, nc in neighbors(r, c):\n            new_path = dfs(nr, nc, path + [grid[nr][nc]], k - 1)\n            if new_path[-1] < min_path[-1]:\n                min_path = new_path"
      },
      {
        "field": "incorrect_code",
        "start_line": 15,
        "end_line": 15,
        "quote": "        return min_path"
      },
      {
        "field": "incorrect_code",
        "start_line": 17,
        "end_line": 17,
        "quote": "    min_path = [float('inf')] * k"
      },
      {
        "field": "incorrect_code",
        "start_line": 18,
        "end_line": 22,
        "quote": "    for r in range(len(grid)):\n        for c in range(len(grid[0])):\n            path = dfs(r, c, [grid[r][c]], k - 1)\n            if path[-1] < min_path[-1]:\n                min_path = path"
      },
      {
        "field": "incorrect_code",
        "start_line": 23,
        "end_line": 23,
        "quote": "    return min_path"
      }
    ]
  }
]
````

## C12 — Incorrect result assembly or return contract

The returned result has the wrong structure, components, multiplicity, formatting or object kind, including incorrect placement of values in an assembled result.

- Include: Missing separators or markers, malformed message substitution, wrong list/tuple/scalar/function return form.
Dropped or duplicated output elements, or incorrectly interleaved output components.
Returning a proxy object rather than the specified result representation.
- Exclude: No completed return in an unfinished implementation: C01.
An incorrect numeric value alone: identify its mechanism instead.
Domain encoding or parsing transformations: C10; output ordering alone: C11.
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 36; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "3",
    "rationale": "Places delimiters only at endpoints and drops the last original number.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 1,
        "end_line": 1,
        "quote": "from typing import List"
      },
      {
        "field": "incorrect_code",
        "start_line": 11,
        "end_line": 11,
        "quote": "    return [delimeter] + [numbers[i] for i in range(len(numbers) - 1)] + [delimeter]"
      }
    ]
  },
  {
    "case_id": "234",
    "rationale": "Returns an inner function object rather than an encrypted string.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 12,
        "end_line": 12,
        "quote": "    alphabet = 'abcdefghijklmnopqrstuvwxyz'"
      },
      {
        "field": "incorrect_code",
        "start_line": 15,
        "end_line": 15,
        "quote": "        rotated_alphabet = alphabet[alphabet.index(s)%len(alphabet)]"
      },
      {
        "field": "incorrect_code",
        "start_line": 16,
        "end_line": 16,
        "quote": "        return rotated_alphabet + s"
      },
      {
        "field": "incorrect_code",
        "start_line": 17,
        "end_line": 17,
        "quote": "    return encrypt"
      }
    ]
  },
  {
    "case_id": "84",
    "rationale": "Interpolates position indices into an incomplete template instead of replacing every i with the odd-digit count.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 13,
        "end_line": 13,
        "quote": "    return [\"the number of odd elements \" + str(len([i for i in lst[j] if int(i) % 2 == 1])) + \"n the str\" + str(j + 1) + \" of the \" + str(j + 1) + \"nput.\" for j in range(len(lst))]"
      }
    ]
  },
  {
    "case_id": "494",
    "rationale": "Omits the trailing db marker and represents zero with no binary digit.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 13,
        "end_line": 13,
        "quote": "    binary = \"\""
      },
      {
        "field": "incorrect_code",
        "start_line": 14,
        "end_line": 16,
        "quote": "    while decimal > 0:\n        binary = str(decimal % 2) + binary\n        decimal = decimal // 2"
      },
      {
        "field": "incorrect_code",
        "start_line": 17,
        "end_line": 17,
        "quote": "    return \"db\" + binary"
      }
    ]
  }
]
````

## C13 — Unhandled boundary or exceptional input

A valid boundary case or an explicitly specified invalid-input case bypasses necessary handling, producing an exception or a result contrary to that case's contract.

- Include: Empty or all-filtered collections, zero-sized selection, zero/negative digit enumeration, equal operands.
Insufficient resources requiring saturation, or malformed inputs for which the contract requires a Boolean/sentinel.
A boundary guard that checks only the original collection rather than a derived empty collection.
- Exclude: General indexing mistakes affecting ordinary traversal: C07.
Wrong recurrence base states: C08.
Do not assume a required behavior for inputs explicitly excluded by the task; record ambiguity where the domain is unclear.
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 20; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "111",
    "rationale": "For a zero-only list both filtered groups are empty, but min(positives) is still evaluated.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 13,
        "end_line": 28,
        "quote": "    if len(lst) == 0:\n        return (None, None)\n    else:\n        negatives = []\n        positives = []\n        for i in lst:\n            if i < 0:\n                negatives.append(i)\n            elif i > 0:\n                positives.append(i)\n        if len(negatives) == 0:\n            return (None, min(positives))\n        elif len(positives) == 0:\n            return (max(negatives), None)\n        else:\n            return (max(negatives), min(positives))"
      }
    ]
  },
  {
    "case_id": "551",
    "rationale": "Selects the smallest k elements; at k=0 returns the original array instead of an empty result.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 26,
        "end_line": 27,
        "quote": "    if not arr or k == 0:\n        return arr"
      },
      {
        "field": "incorrect_code",
        "start_line": 29,
        "end_line": 29,
        "quote": "    arr.sort()"
      },
      {
        "field": "incorrect_code",
        "start_line": 30,
        "end_line": 30,
        "quote": "    return arr[:k]"
      }
    ]
  },
  {
    "case_id": "737",
    "rationale": "Consumes need even when stock is smaller, producing negative stock.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 30,
        "end_line": 30,
        "quote": "    return [number + need, remaining - need]"
      }
    ]
  },
  {
    "case_id": "278",
    "rationale": "Parses malformed dates without guarding conversions or component count, ignores month-specific day limits, and invents a year>=1900 restriction.",
    "evidence": [
      {
        "field": "incorrect_code",
        "start_line": 21,
        "end_line": 21,
        "quote": "    date_parts = date.split('-')"
      },
      {
        "field": "incorrect_code",
        "start_line": 22,
        "end_line": 22,
        "quote": "    month = int(date_parts[0])"
      },
      {
        "field": "incorrect_code",
        "start_line": 23,
        "end_line": 23,
        "quote": "    day = int(date_parts[1])"
      },
      {
        "field": "incorrect_code",
        "start_line": 24,
        "end_line": 24,
        "quote": "    year = int(date_parts[2])"
      },
      {
        "field": "incorrect_code",
        "start_line": 25,
        "end_line": 26,
        "quote": "    if month < 1 or month > 12:\n        return False"
      },
      {
        "field": "incorrect_code",
        "start_line": 27,
        "end_line": 28,
        "quote": "    if day < 1 or day > 31:\n        return False"
      },
      {
        "field": "incorrect_code",
        "start_line": 29,
        "end_line": 30,
        "quote": "    if year < 1900:\n        return False"
      },
      {
        "field": "incorrect_code",
        "start_line": 31,
        "end_line": 31,
        "quote": "    return True"
      }
    ]
  }
]
````

## Files

- `codebook.md`, `codebook.json`, `codebook.csv`: definitions and complete reverse memberships.
- `assignments.json`, `assignments.csv`: one record per artifact, including decisions and evidence.
- `taxonomy.json`: category tree with every code as a leaf.
- `results.json`: supplied full documents aligned to their assignments.

## Original codebook

The original codebook text below preserves run-specific scope, combination rules and qualifications. Links and filenames in that historical text describe the original package; use the seven files above for the normalized interface. The exact original text is also stored in metadata extensions.

# Code errors — inductive codebook (GPT6-2)

557 artifacts · 687 source records · 150 tasks · 13 codes · 706 artifact–code assignments.

Each artifact has at least one code. Codes describe distinct observed mechanisms and may co-occur. Case 729 is conditional on an explicitly recorded interpretation of conflicting task requirements. This is a single-assistant source-based analysis, not a human-validated gold codebook.

| Code | Name | Artifacts |
|---|---|---:|
| C01 | Incomplete or nonfunctional implementation | 106 |
| C02 | Unavailable symbol or dependency | 46 |
| C03 | Incompatible operation or API use | 16 |
| C04 | Wrong computational target or unit of analysis | 122 |
| C05 | Omitted requirement or processing step | 93 |
| C06 | Incorrect decision condition | 54 |
| C07 | Incorrect traversal or positional coverage | 40 |
| C08 | Incorrect state evolution or termination | 29 |
| C09 | Incorrect arithmetic or numerical treatment | 32 |
| C10 | Incorrect representation or transformation | 68 |
| C11 | Incorrect ordering or selection priority | 44 |
| C12 | Incorrect result assembly or return contract | 36 |
| C13 | Unhandled boundary or exceptional input | 20 |

## C01 — Incomplete or nonfunctional implementation

实现未完成或缺乏有效处理

The supplied program lacks a completed task-solving path: its body is absent, its source is truncated, its general computation never returns a result, or it substitutes an input-independent placeholder for the requested behavior.

**Include**

- Pass-only or documentation-only bodies; unfinished literals, expressions or blocks.
- Repeated or partial statements without a completed computation and return.
- Constant placeholder output with no substantive implementation of the task.

**Exclude / distinguish**

- A missing local operation in an otherwise substantive algorithm: C05.
- An implemented calculation that solves a different problem: C04.
- A missing symbol used by otherwise interpretable logic: C02; co-code only if lack of a completed result is separate.

**Representative cases**

- Case 1: Function body is pass; no grouping behavior is implemented.
- Case 17: Repeated coefficient manipulation ends in an incomplete comprehension without finding or returning a root.
- Case 77: Returns an empty constant instead of processing nonempty inputs.
- Case 270: Calls undefined count_ones and repeats bit-length updates without returning an ordering.

Supporting artifacts: **106**. Exact source excerpts and all supporting IDs are in `codebook.json`; per-artifact requirements, evidence and caveats are in `assignments.json`.

## C02 — Unavailable symbol or dependency

引用未提供的符号或依赖

The supplied program requires a variable, helper, module or imported name that is not bound in the context provided with the artifact.

**Include**

- Calls to undeclared helpers or unimported modules.
- Misspelled or out-of-scope names needed for execution.

**Exclude / distinguish**

- A present object with an unsupported operation: C03.
- An unfinished token in truncated source, without a separately established dependency: C01.
- Do not assume an external execution harness supplies the missing name; state this context limit.

**Representative cases**

- Case 426: Calls math.floor without importing or defining math in the supplied program.
- Case 79: Calls is_palindrome and is_even without defining or importing them.
- Case 356: Uses undefined c in result construction, lacks a return, and max on empty counts fails the specified empty case.
- Case 138: Calls hashlib.md5 without importing hashlib.

Supporting artifacts: **46**. Exact source excerpts and all supporting IDs are in `codebook.json`; per-artifact requirements, evidence and caveats are in `assignments.json`.

## C03 — Incompatible operation or API use

操作与数据类型或 API 不匹配

An operation, method or API is applied to an object or argument structure that cannot provide the intended behavior under Python's type and API semantics.

**Include**

- Arithmetic on character strings, numeric objects treated as sequences, unsupported container methods.
- Invalid argument or subscript types; list multiplication used where scalar arithmetic is required.

**Exclude / distinguish**

- An undeclared object or function: C02.
- A valid operation with the wrong numeric formula: C09.
- Domain-specific text or numeric representation conversion errors are C10 when that explains the failure without an additional API misuse.

**Representative cases**

- Case 146: Calls mean on individual numeric elements, which do not supply that method.
- Case 435: Applies bitwise XOR directly to character strings.
- Case 208: Treats integer x as a sequence with length and slicing.
- Case 275: Uses a list of indices as a Python list subscript and omits the even-position eligibility condition.

Supporting artifacts: **16**. Exact source excerpts and all supporting IDs are in `codebook.json`; per-artifact requirements, evidence and caveats are in `assignments.json`.

## C04 — Wrong computational target or unit of analysis

计算目标或处理单位偏离要求

The implementation computes a different property, uses the wrong entities or aggregation level, or replaces the required relation with a non-equivalent proxy.

**Include**

- Word length instead of consonant count; whole-number properties instead of digit properties; indices instead of values.
- Whole-collection totals instead of per-group calculations; ordinary factorial instead of product of factorials.
- Checking a different mathematical property, such as parity instead of primality.

**Exclude / distinguish**

- The intended quantity is computed with a wrong local formula: C09.
- A correct target lacks one additional eligibility check: C05.
- A recognizably correct predicate has an incorrect threshold or Boolean relation: C06.
- A ranking objective alone is wrong: C11.

**Representative cases**

- Case 271: Filters by whole-word length rather than number of consonants.
- Case 359: Rounds total pooled water once instead of rounding each well separately before summing.
- Case 114: Computes ordinary factorial rather than the product of factorials.
- Case 593: Uses parity as a substitute for primality.

Supporting artifacts: **122**. Exact source excerpts and all supporting IDs are in `codebook.json`; per-artifact requirements, evidence and caveats are in `assignments.json`.

## C05 — Omitted requirement or processing step

遗漏必要条件、分支或处理步骤

A substantive implementation performs part of the requested task but leaves out a required condition, operation, branch or explicitly stated implementation constraint.

**Include**

- Missing an eligibility filter, required transformation, alternate allowed mode, or part of a conjunction.
- Implementing only some explicitly permitted cases; ignoring a stated no-recursion constraint.
- Dropping the contribution of otherwise valid unmatched elements.

**Exclude / distinguish**

- The whole implementation is absent or a placeholder: C01.
- An existing condition is wrong rather than absent: C06.
- Prefer C07 for traversal coverage, C10 for representation-specific normalization, C11 for tie-breaking, and C13 for exceptional-input guards; do not add C05 again for the same omission.

**Representative cases**

- Case 55: Sums odd-index values without requiring those values to be even.
- Case 83: Returns all character counts without retaining only the maximum-frequency characters.
- Case 137: Omits reversal when the string has no letters.
- Case 721: Drops entries whose indices are multiples of neither three nor four.

Supporting artifacts: **93**. Exact source excerpts and all supporting IDs are in `codebook.json`; per-artifact requirements, evidence and caveats are in `assignments.json`.

## C06 — Incorrect decision condition

判断条件、阈值或分支优先级错误

A condition controlling eligibility, branching or result emission uses an incorrect relation, threshold, logical combination or precedence, although its intended decision can be identified.

**Include**

- Strict versus inclusive comparisons, reversed predicates, tautologies and contradictions.
- Unjustified restrictions and incorrect branch precedence.
- Result emission guarded by a condition unrelated to when that result is required.

**Exclude / distinguish**

- An absent condition: C05, or C13 for exceptional-input handling.
- A predicate for a fundamentally different property: C04.
- A faulty state reset or recurrence: C08; traversal bounds: C07.

**Representative cases**

- Case 151: Appends only when the count of new maxima equals the full length; zero initialization also invalidates negative maxima.
- Case 176: Includes zero despite requiring strictly positive numbers.
- Case 281: Requires strict increase, rejecting the explicitly permitted pair of equal values.
- Case 418: Gives cubing priority at indices divisible by both three and four, reversing the required precedence.

Supporting artifacts: **54**. Exact source excerpts and all supporting IDs are in `codebook.json`; per-artifact requirements, evidence and caveats are in `assignments.json`.

## C07 — Incorrect traversal or positional coverage

遍历范围、位置或候选覆盖错误

Iteration, indexing or candidate enumeration visits the wrong positions, omits required candidates, or accesses positions outside the applicable sequence bounds.

**Include**

- Off-by-one endpoints, incorrect index parity, wrong scan direction or returned neighboring index.
- Considering only adjacent or fixed candidates when arbitrary candidates are required.
- Skipping overlapping matches or forbidding permitted revisits.

**Exclude / distinguish**

- Correctly visited values are ranked incorrectly: C11.
- A failure restricted to an empty, zero-sized or short boundary input requiring a guard: C13.
- Wrong loop state or nontermination: C08; wrong semantic object being traversed: C04.

**Representative cases**

- Case 141: Tests only two fixed pairs and indexes four positions even when the list is shorter.
- Case 165: Advances by substring length and skips possible overlapping or unaligned matches.
- Case 375: Returns i-1 instead of the index i of the descending element.
- Case 368: Uses unimported heapq; globally marks cells visited despite allowed revisits and prioritizes last values rather than whole paths.

Supporting artifacts: **40**. Exact source excerpts and all supporting IDs are in `codebook.json`; per-artifact requirements, evidence and caveats are in `assignments.json`.

## C08 — Incorrect state evolution or termination

状态初始化、更新或终止错误

Stateful or recursive computation uses incorrect seeds, updates, recurrence dependencies or stopping behavior, so intermediate state no longer represents the required computation.

**Include**

- Wrong sequence bases, corrupted rolling state, future-state reads before initialization.
- Recursion with no decreasing argument or unsuccessful-cycle termination.
- Resetting a running aggregate on the wrong sign; losing associations when independently updating linked structures.

**Exclude / distinguish**

- A stateless formula error: C09.
- An output-only container shape problem: C12.
- Wrong loop index bounds without a state-evolution defect: C07.

**Representative cases**

- Case 334: Starts recurrence before all four base states and overwrites the previous d before shifting state.
- Case 81: Recursively rotates until sorted with no unsuccessful-cycle termination; unsortable rotations recurse indefinitely.
- Case 358: Resets negative running sums rather than positive ones when minimizing contiguous sum.
- Case 732: Sorts strength values apart from their names and selects index zero of the sorted scores, losing the score-to-extension association.

Supporting artifacts: **29**. Exact source excerpts and all supporting IDs are in `codebook.json`; per-artifact requirements, evidence and caveats are in `assignments.json`.

## C09 — Incorrect arithmetic or numerical treatment

算式、运算顺序或数值处理错误

The intended quantity is recognizable, but its mathematical expression, numeric operator, rounding, precision treatment or operation order is wrong.

**Include**

- Missing factors or roots, double counting, incorrect inclusion–exclusion formulas.
- True division instead of integer digit extraction, wrong rounding convention, operator precedence ignored.
- Numerical stopping or exactness assumptions that do not ensure the requested numeric result.

**Exclude / distinguish**

- Computing a different quantity altogether: C04.
- Wrong recurrence dependencies or state updates: C08.
- Wrong text encoding, sign representation or alphabet mapping: C10.
- Do not infer numerical instability solely because floating-point arithmetic is used.

**Representative cases**

- Case 485: Returns Heron radicand without taking its square root.
- Case 523: Uses ties-to-even round where halfway values must round away from zero.
- Case 387: Evaluates operators strictly left-to-right instead of respecting algebraic precedence and exponentiation associativity.
- Case 382: Doubles the correctly filtered squared sum without a requested factor of two.

Supporting artifacts: **32**. Exact source excerpts and all supporting IDs are in `codebook.json`; per-artifact requirements, evidence and caveats are in `assignments.json`.

## C10 — Incorrect representation or transformation

表示方式、解析或转换错误

Parsing, normalization, encoding, decoding or symbolic transformation fails to preserve or implement the task's intended meaning.

**Include**

- Wrong delimiters, numeral bases, signed-digit interpretation, character substitutions or case normalization.
- Regex syntax representing the wrong set of strings.
- Incompatible semantic representations such as string digits compared with integer values; failure to normalize interval bounds.

**Exclude / distinguish**

- Only the final message, marker, container or return shape is incorrect: C12.
- Generic unsupported methods or operand types without a representation-specific cause: C03.
- A missing unrelated eligibility filter: C05.

**Representative cases**

- Case 163: Counts case-sensitive characters without required case normalization.
- Case 80: Taking absolute values discards the required negative sign on the leading digit.
- Case 379: Uses a regex character class instead of extension alternatives, admitting invalid extensions and restricting allowed basename characters.
- Case 132: Additive Roman conversion omits required subtractive forms such as iv and ix.

Supporting artifacts: **68**. Exact source excerpts and all supporting IDs are in `codebook.json`; per-artifact requirements, evidence and caveats are in `assignments.json`.

## C11 — Incorrect ordering or selection priority

排序、择优规则或平局处理错误

The program orders values or chooses a preferred candidate using the wrong direction, ranking key, key precedence or tie-breaking rule.

**Include**

- Selecting first, smallest or most frequent when a different optimum is required.
- Ignoring a secondary key, reversing requested output order, comparing only the last component of a lexicographic path.
- Sorting positions that must remain in original order.

**Exclude / distinguish**

- A search never visits required candidates: C07.
- A generic property proxy outside ordering or selection: C04.
- A wrong key caused specifically by signed-digit interpretation: C10, without a redundant C11 label.

**Representative cases**

- Case 157: Sorts ascending by length then returns the shortest entry.
- Case 547: Sorts only by set-bit count and omits the numeric tie-break; prose and reference establish the tie-break despite inconsistent examples.
- Case 361: Returns the largest k elements in descending instead of required increasing order.
- Case 415: Compares only final path values rather than lexicographic sequences.

Supporting artifacts: **44**. Exact source excerpts and all supporting IDs are in `codebook.json`; per-artifact requirements, evidence and caveats are in `assignments.json`.

## C12 — Incorrect result assembly or return contract

结果组装或返回形式不符合要求

The returned result has the wrong structure, components, multiplicity, formatting or object kind, including incorrect placement of values in an assembled result.

**Include**

- Missing separators or markers, malformed message substitution, wrong list/tuple/scalar/function return form.
- Dropped or duplicated output elements, or incorrectly interleaved output components.
- Returning a proxy object rather than the specified result representation.

**Exclude / distinguish**

- No completed return in an unfinished implementation: C01.
- An incorrect numeric value alone: identify its mechanism instead.
- Domain encoding or parsing transformations: C10; output ordering alone: C11.

**Representative cases**

- Case 3: Places delimiters only at endpoints and drops the last original number.
- Case 234: Returns an inner function object rather than an encrypted string.
- Case 84: Interpolates position indices into an incomplete template instead of replacing every i with the odd-digit count.
- Case 494: Omits the trailing db marker and represents zero with no binary digit.

Supporting artifacts: **36**. Exact source excerpts and all supporting IDs are in `codebook.json`; per-artifact requirements, evidence and caveats are in `assignments.json`.

## C13 — Unhandled boundary or exceptional input

边界或异常输入处理缺失

A valid boundary case or an explicitly specified invalid-input case bypasses necessary handling, producing an exception or a result contrary to that case's contract.

**Include**

- Empty or all-filtered collections, zero-sized selection, zero/negative digit enumeration, equal operands.
- Insufficient resources requiring saturation, or malformed inputs for which the contract requires a Boolean/sentinel.
- A boundary guard that checks only the original collection rather than a derived empty collection.

**Exclude / distinguish**

- General indexing mistakes affecting ordinary traversal: C07.
- Wrong recurrence base states: C08.
- Do not assume a required behavior for inputs explicitly excluded by the task; record ambiguity where the domain is unclear.

**Representative cases**

- Case 111: For a zero-only list both filtered groups are empty, but min(positives) is still evaluated.
- Case 551: Selects the smallest k elements; at k=0 returns the original array instead of an empty result.
- Case 737: Consumes need even when stock is smaller, producing negative stock.
- Case 278: Parses malformed dates without guarding conversions or component count, ignores month-specific day limits, and invents a year>=1900 restriction.

Supporting artifacts: **20**. Exact source excerpts and all supporting IDs are in `codebook.json`; per-artifact requirements, evidence and caveats are in `assignments.json`.
