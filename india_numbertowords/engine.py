"""Core engine for number-to-words conversion."""

import re


class NumberEngine:
    """Engine for converting numbers to words using language-specific data."""
    
    def __init__(self, lang_data):
        """
        Initialize the engine with language data.
        
        Args:
            lang_data: Dictionary containing atoms, magnitudes, alphabet, etc.
        """
        self.atoms = lang_data['atoms']
        self.magnitudes = lang_data['magnitudes']
        self.alphabet = lang_data.get('alphabet', {})
        self.decimal_point = lang_data.get('decimal_point', 'point')
        self.separator = lang_data.get('separator', ' ')
    
    def convert(self, input_val, mode=None):
        """
        Convert input to words.
        
        Args:
            input_val: int or str. The number to convert.
            mode: str (optional). 'currency' or 'individual'.
        
        Returns:
            str: The number in words.
        """
        # Parse input and detect mode
        parsed = self._parse_input(input_val, mode)
        
        # Route to appropriate handler
        if parsed['mode'] == 'individual':
            return self._convert_individual(parsed['value'])
        elif parsed['has_decimal']:
            return self._convert_decimal(parsed['integer'], parsed['fractional'])
        else:
            return self._convert_currency(parsed['value'])
    
    def _parse_input(self, input_val, mode_override):
        """
        Parse input and apply smart heuristics to determine mode.
        
        Args:
            input_val: The input value (int or str).
            mode_override: User-specified mode (overrides heuristics).
        
        Returns:
            dict: Parsed information including mode, value, decimal parts.
        """
        result = {
            'mode': mode_override or 'currency',
            'has_decimal': False,
            'value': None,
            'integer': None,
            'fractional': None
        }
        
        # Convert to string
        text = str(input_val)
        
        # Check for alphanumeric FIRST (before decimal check)
        # This handles cases like "v1.2.3" correctly
        if any(c.isalpha() for c in text):
            result['mode'] = 'individual'
            result['value'] = text
            return result
        
        # Check for decimal (only if no letters)
        if '.' in text:
            parts = text.split('.')
            # Clean the integer part
            int_part = parts[0].replace(',', '').replace(' ', '').replace('-', '')
            result['has_decimal'] = True
            result['integer'] = int(int_part) if int_part and int_part.isdigit() else 0
            result['fractional'] = parts[1]
            return result
        
        # Smart heuristics (if no mode override)
        if mode_override is None:
            # Leading zeros - check BEFORE cleaning
            if text.startswith('0') and len(text) > 1 and text.replace(',', '').replace(' ', '').replace('-', '').isdigit():
                result['mode'] = 'individual'
                result['value'] = text
                return result
            # Separators (space, hyphen) - but not just commas
            elif ' ' in text or '-' in text:
                result['mode'] = 'individual'
            # Commas = currency
            elif ',' in text:
                result['mode'] = 'currency'
        
        # Clean and convert
        cleaned = text.replace(',', '').replace('-', '').replace(' ', '')
        if cleaned.isdigit():
            result['value'] = int(cleaned)
        else:
            # Fallback to individual for non-numeric
            result['value'] = text
            result['mode'] = 'individual'
        
        return result
    
    def _convert_currency(self, number):
        """
        Convert number using currency/standard mode (recursive decomposition).
        
        Args:
            number: int. The number to convert.
        
        Returns:
            str: The number in words.
        """
        # Base case: atom lookup
        if number in self.atoms:
            return self.atoms[number]
        
        # Recursive case: find magnitude
        for value, name in self.magnitudes:
            if number >= value:
                quotient, remainder = divmod(number, value)
                result = f"{self._convert_currency(quotient)}{self.separator}{name}"
                if remainder > 0:
                    result += f"{self.separator}{self._convert_currency(remainder)}"
                return result.strip()
        
        # Fallback: split digits (shouldn't reach here with proper atoms 0-99)
        return self._convert_individual(str(number))
    
    def _convert_individual(self, text):
        """
        Convert text character-by-character (individual mode).
        
        Args:
            text: str. The text to convert.
        
        Returns:
            str: Each character converted to words.
        """
        result = []
        text = str(text)
        
        for char in text:
            if char.isdigit():
                digit = int(char)
                result.append(self.atoms[digit])
            elif char.isalpha():
                result.append(self.alphabet.get(char.upper(), char))
            # Skip separators like '-', ' ', etc.
        
        return self.separator.join(result)
    
    def _convert_decimal(self, integer_part, fractional_part):
        """
        Convert decimal number.
        
        Args:
            integer_part: int. The integer part.
            fractional_part: str. The fractional part (as string to preserve leading zeros).
        
        Returns:
            str: The decimal number in words.
        """
        int_words = self._convert_currency(integer_part)
        frac_words = self._convert_individual(fractional_part)
        return f"{int_words}{self.separator}{self.decimal_point}{self.separator}{frac_words}"
