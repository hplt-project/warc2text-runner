import re

class Patterns:
    URL_PATTERN_STR = r"""((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"""
    SMILEYS_PATTERN_STR = r"(\s?:X|:|;|=)(?:-)?(?:\)+|\(|O|D|P|S|\\|\/\s){1,}"
    NUMBERS_PATTERN_STR = r"(^|\s)(-?\d+([.,]?\d+)*)"
    ## these patterns are probably not worthwhile for our crawl since they're for twitter
    # HASHTAG_PATTERN = re.compile(r'#\w*')
    # MENTION_PATTERN = re.compile(r'@\w*')
    # RESERVED_WORDS_PATTERN = re.compile(r'\b(?<![@#])(RT|FAV)\b')

    URL_SMILEY_NUMS_PATTERN = re.compile(f"{URL_PATTERN_STR}|{SMILEYS_PATTERN_STR}|{NUMBERS_PATTERN_STR}", re.IGNORECASE)

    try:
        # UCS-4
        EMOJIS_PATTERN = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
    except re.error:
        # UCS-2
        EMOJIS_PATTERN = re.compile(u'([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])')