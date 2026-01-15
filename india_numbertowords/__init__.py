"""India Number to Words - Convert numbers to words in Indian languages."""

from .engine import NumberEngine
from .languages.hi import HINDI_DATA
from .languages.bn import BENGALI_DATA
from .languages.mr import MARATHI_DATA
from .languages.gu import GUJARATI_DATA
from .languages.te import TELUGU_DATA
from .languages.kn import KANNADA_DATA
from .languages.ta import TAMIL_DATA
from .languages.ml import MALAYALAM_DATA
from .languages.or_lang import ODIA_DATA
from .languages.pa import PUNJABI_DATA
from .languages.as_lang import ASSAMESE_DATA
from .languages.ur import URDU_DATA
from .languages.ne import NEPALI_DATA
from .languages.sa import SANSKRIT_DATA
from .languages.mai import MAITHILI_DATA
from .languages.en import ENGLISH_DATA

__version__ = "0.2.0"

# Initialize language engines
_engines = {
    'hi': NumberEngine(HINDI_DATA),
    'bn': NumberEngine(BENGALI_DATA),
    'mr': NumberEngine(MARATHI_DATA),
    'gu': NumberEngine(GUJARATI_DATA),
    'te': NumberEngine(TELUGU_DATA),
    'kn': NumberEngine(KANNADA_DATA),
    'ta': NumberEngine(TAMIL_DATA),
    'ml': NumberEngine(MALAYALAM_DATA),
    'or': NumberEngine(ODIA_DATA),
    'pa': NumberEngine(PUNJABI_DATA),
    'as': NumberEngine(ASSAMESE_DATA),
    'ur': NumberEngine(URDU_DATA),
    'ne': NumberEngine(NEPALI_DATA),
    'sa': NumberEngine(SANSKRIT_DATA),
    'mai': NumberEngine(MAITHILI_DATA),
    'en': NumberEngine(ENGLISH_DATA),
}

# Language names for reference
SUPPORTED_LANGUAGES = {
    'hi': 'Hindi',
    'bn': 'Bengali',
    'mr': 'Marathi',
    'gu': 'Gujarati',
    'te': 'Telugu',
    'kn': 'Kannada',
    'ta': 'Tamil',
    'ml': 'Malayalam',
    'or': 'Odia',
    'pa': 'Punjabi',
    'as': 'Assamese',
    'ur': 'Urdu',
    'ne': 'Nepali',
    'sa': 'Sanskrit',
    'mai': 'Maithili',
    'en': 'English',
}

def num2words(input_val, lang='hi', mode=None):
    """
    Convert a number to words in the specified Indian language.
    
    Args:
        input_val: int or str. The number to convert.
        lang: str. Language code (default 'hi' for Hindi).
              Supported: hi, bn, mr, gu, te, kn, ta, ml, or, pa, as, ur, ne, sa, mai, en
        mode: str (optional). 'currency' or 'individual'. 
              If None, inferred from input_val heuristics.
    
    Returns:
        str: The number in words.
    
    Examples:
        >>> num2words(42, lang='hi')
        'बयालीस'
        >>> num2words(42, lang='bn')
        'বিয়াল্লিশ'
        >>> num2words(42, lang='en')
        'forty two'
    """
    if lang not in _engines:
        available = ', '.join(sorted(_engines.keys()))
        raise ValueError(f"Language '{lang}' not supported. Available: {available}")
    
    return _engines[lang].convert(input_val, mode)


def get_supported_languages():
    """Return dict of supported language codes and names."""
    return SUPPORTED_LANGUAGES.copy()

