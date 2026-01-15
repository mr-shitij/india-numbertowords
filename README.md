# India Number to Words

A Python library for converting numbers to words in Indian languages with smart input detection and recursive magnitude decomposition.

## Features

- ✅ **16 Languages**: Hindi, Bengali, Marathi, Gujarati, Telugu, Kannada, Tamil, Malayalam, Odia, Punjabi, Assamese, Urdu, Nepali, Sanskrit, Maithili, English
- ✅ **Smart Mode Detection**: Automatically detects currency vs individual reading
- ✅ **Decimal Numbers**: `"3.14"` → "तीन दशमलव एक चार"
- ✅ **Alphanumeric**: `"AB123"` → "ए बी एक दो तीन"
- ✅ **Indian Numbering**: Crore, Lakh, Thousand, Hundred
- ✅ **Leading Zeros**: `"007"` → "शून्य शून्य सात"

## Installation

```bash
pip install -e .
```

## Quick Start

```python
from india_numbertowords import num2words, get_supported_languages

# See all supported languages
print(get_supported_languages())
# {'hi': 'Hindi', 'bn': 'Bengali', 'mr': 'Marathi', ...}

# Basic numbers in any language
num2words(42, lang='hi')   # "बयालीस"
num2words(42, lang='bn')   # "বিয়াল্লিশ"
num2words(42, lang='en')   # "forty two"

# Large numbers (Indian system)
num2words(12345, lang='hi')  # "बारह हज़ार तीन सौ पैंतालीस"

# With formatting (auto-detected)
num2words("1,23,456", lang='hi')  # "एक लाख तेईस हज़ार..."
num2words("007", lang='hi')       # "शून्य शून्य सात"

# Explicit individual mode
num2words(123, lang='hi', mode='individual')  # "एक दो तीन"

# Decimals
num2words("3.14", lang='hi')  # "तीन दशमलव एक चार"

# Alphanumeric
num2words("AB123", lang='hi')  # "ए बी एक दो तीन"
```

## Supported Languages

| Code | Language | Code | Language |
|:-----|:---------|:-----|:---------|
| `hi` | Hindi | `ml` | Malayalam |
| `bn` | Bengali | `or` | Odia |
| `mr` | Marathi | `pa` | Punjabi |
| `gu` | Gujarati | `as` | Assamese |
| `te` | Telugu | `ur` | Urdu |
| `kn` | Kannada | `ne` | Nepali |
| `ta` | Tamil | `sa` | Sanskrit |
| `mai` | Maithili | `en` | English |

---

## Architecture

### Overview

This library provides a robust, scalable, and predictable way to convert numbers into words for Indian languages. It uses a **Recursive Magnitude Decomposition Engine**.

### Core Philosophy

1. **Strict Separation of Concerns**:
   - **Engine**: Generic logic for breaking numbers down (Recursive).
   - **Data**: Language-specific vocabulary (Atoms, Magnitudes).
2. **Predictability**: The library behavior is deterministic based on input format and explicit user configuration.

### The Engine (`engine.py`)

The core reading logic is based on **Recursive Decomposition**.

#### Algorithm `convert(number)`

1. **Base Case (Atoms)**:
   - Check if `number` exists in the language's `atoms` dictionary (e.g., 0-99).
   - If yes, return the word immediately.

2. **Recursive Step (Magnitudes)**:
   - Iterate through the language's `magnitudes` (descending order).
   - *Standard Indian Magnitudes*:
     - `Crore` (1,00,00,000)
     - `Lakh` (1,00,000)
     - `Thousand` (1,000)
     - `Hundred` (100)
   - Find the largest magnitude `M` where `number >= M`.
   - Compute:
     - `Quotient = number // M` (How many of this magnitude?)
     - `Remainder = number % M` (What's left?)
   - **Result**: `convert(Quotient) + " " + Name(M)`
   - If `Remainder > 0`: Append `convert(Remainder)`

3. **Fallback**: If no magnitude fits and not an atom (unlikely), split into digits.

#### Decimal & Alphanumeric Handling

1. **Decimal Points**: When a `.` is detected:
   - Split the number into integer and fractional parts.
   - Integer part: Use standard Currency/Individual logic.
   - Decimal point: Read as "Point" (or language equivalent).
   - Fractional part: Read each digit individually.
   - Example: `"3.14"` → "Three Point One Four"

2. **Alphanumeric Characters**: When letters (A-Z, a-z) are detected:
   - Automatically switch to **Individual mode**.
   - Read each character: Numbers as digits, Letters as alphabet names.
   - Example: `"AB123"` → "A B One Two Three"

---

### Smart Heuristics (Input Logic)

How do we decide whether to read as "Currency" (One Hundred) or "Individual" (One Zero Zero)?
We use **Smart Input Sniffing** on string inputs.

#### The Decision Matrix

| Input Feature | Example | Inferred Mode | Reasoning |
|:--------------|:--------|:--------------|:----------|
| **Commas** | `"1,00,000"` | `Currency` | User formatted it as a value. |
| **Separators** | `"98-76"`, `"12 34"` | `Individual` | Phone number / grouping pattern. |
| **Leading Zeros** | `"007"` | `Individual` | "Seven" loses the precision of "007". |
| **Clean Digits** | `"1234"` | `Currency` | Default assumption for values. |
| **Integer Type** | `1234` | `Currency` | Formatting lost, assume value. |

*Note: The user can ALWAYS override this by passing `mode='individual'` or `mode='currency'` explicitly.*

---

### Language Configuration

Adding a language requires **Zero Logic**. It only needs a data file.

#### Structure (`languages/hi.py`)

```python
data = {
    # 1. Atoms: Unique words (usually 0-99 in Indian languages)
    "atoms": {
        0: "shunya",
        1: "ek",
        # ...
        99: "ninyanve"
    },
    
    # 2. Magnitudes: The breakpoints
    "magnitudes": [
        (10000000, "karod"), # Crore
        (100000, "lakh"),    # Lakh
        (1000, "hazaar"),    # Thousand
        (100, "sau")         # Hundred
    ],
    
    # 3. Alphabet: For alphanumeric support
    "alphabet": {
        "A": "ए", "B": "बी", ...
    },
    
    # 4. Connectors
    "decimal_point": "दशमलव",
    "separator": " "
}
```

---

### API Design

```python
def num2words(input_val, lang="hi", mode=None):
    """
    Args:
        input_val: int or str. The number to convert.
        lang: str. Language code (default 'hi').
        mode: str (optional). 'currency' or 'individual'. 
              If None, inferred from input_val heuristics.
    """
```

---

## Detailed Examples (Hindi)

### Currency Mode Examples

| Input | Output (Hindi) | Explanation |
|:------|:---------------|:------------|
| `42` | "बयालीस" (Bayalis) | Direct atom lookup (0-99) |
| `100` | "एक सौ" (Ek Sau) | 1 × Hundred |
| `150` | "एक सौ पचास" (Ek Sau Pachas) | 1 × Hundred + 50 |
| `1,000` | "एक हज़ार" (Ek Hazaar) | 1 × Thousand |
| `1,23,456` | "एक लाख तेईस हज़ार चार सौ छप्पन" | 1 Lakh + 23 Thousand + 4 Hundred + 56 |
| `10,00,000` | "दस लाख" (Das Lakh) | 10 × Lakh |
| `1,00,00,000` | "एक करोड़" (Ek Karod) | 1 × Crore |
| `12,34,56,789` | "बारह करोड़ चौंतीस लाख छप्पन हज़ार सात सौ नवासी" | Full decomposition |

### Individual Mode Examples

| Input | Output (Hindi) | Trigger |
|:------|:---------------|:--------|
| `"007"` | "शून्य शून्य सात" (Shunya Shunya Saat) | Leading zeros |
| `"98-76"` | "नौ आठ सात छह" (Nau Aath Saat Chhe) | Separator detected |
| `"12 34"` | "एक दो तीन चार" (Ek Do Teen Chaar) | Space separator |
| `mode='individual'` with `123` | "एक दो तीन" (Ek Do Teen) | Explicit override |

### Smart Heuristic Detection

| Input String | Detected Mode | Reasoning |
|:-------------|:--------------|:----------|
| **Currency Patterns** |||
| `"1,00,000"` | Currency | Indian comma formatting (Lakh) |
| `"12,34,567"` | Currency | Indian comma pattern (Lakh system) |
| `"1,000,000"` | Currency | International comma pattern (Million) |
| `"₹1,50,000"` | Currency | Currency symbol + Indian formatting |
| `"Rs. 25,000"` | Currency | Currency prefix + commas |
| `123` (int) | Currency | Integer type always defaults to currency |
| `"100"` | Currency | No leading zero, standard number |
| `"9876543210"` | Currency | Clean 10-digit string (ambiguous - see note) |
| **Individual/Code Patterns** |||
| `"007"` | Individual | Leading zeros preserve information |
| `"0042"` | Individual | Leading zeros indicate code/ID |
| `"00"` | Individual | All zeros with leading zero |
| `"123-456-7890"` | Individual | Hyphen separators indicate grouping |
| `"98 76 54 32 10"` | Individual | Space separators (phone number style) |
| `"1234 5678 9012 3456"` | Individual | Space grouping (credit card style) |
| `"+91-98765-43210"` | Individual | Mixed separators with country code |
| **Indian-Specific Use Cases** |||
| `"1234-5678-9012"` | Individual | Aadhaar number format (with hyphens) |
| `"123456789012"` | Currency | Aadhaar without separators (needs explicit mode) |
| `"560001"` | Currency | PIN code (6 digits, no leading zero) |
| `"080-12345678"` | Individual | Landline with STD code |
| `"022 1234 5678"` | Individual | Landline with spaces (Mumbai style) |
| **Decimal Numbers** |||
| `"3.14"` | Currency | Decimal with point (reads "Three Point One Four") |
| `"1,234.56"` | Currency | Currency format with decimal |
| `"0.5"` | Currency | Decimal less than one |
| **Alphanumeric & Mixed** |||
| `"v1.2.3"` | Individual | Version number (alphanumeric with dots) |
| `"SBIN0001234"` | Individual | Bank code (letters + numbers) |
| `"ABCDE1234F"` | Individual | ID with mixed letters and numbers |
| `"AB-123-CD"` | Individual | Alphanumeric with separators |
| **Edge Cases & Ambiguous** |||
| `"2024"` | Currency | Year (but might want individual - use explicit mode) |
| `"192.168.1.1"` | Individual | IP address (dots as separators) |
| `"1,234"` | Currency | Ambiguous comma (could be decimal in EU) |
| `"1e6"` | Currency | Scientific notation ("One E Six") |
| `"NaN"` | Individual | Non-numeric text ("N A N") |

**Note on Ambiguous Cases**: 
- `"9876543210"` (10 clean digits): Could be phone or currency. Defaults to **Currency**. For phone numbers, use `mode='individual'` explicitly.
- Years like `"2024"`: Defaults to **Currency** ("Two Thousand Twenty Four"). Use `mode='individual'` for "Two Zero Two Four".
- Account/ID numbers without separators: Default to **Currency**. Always use `mode='individual'` for codes/IDs.
- **Text Prefixes**: The library only processes the numeric/alphanumeric value. Text prefixes like "IFSC:", "PAN:", "OTP:" should be stripped by the caller before passing to the function.

---

## Testing

```bash
python3 tests/test_comprehensive.py
```

34 tests covering all features across all 16 languages.

## License

MIT
