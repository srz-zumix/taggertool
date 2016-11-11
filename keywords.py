import os

cppwords = [  'cpp'
            , 'hpp'
            , 'uint'
            , 'ulong'
            ]

foramtwords = [ 'lld', 'llx', 'llu', 'zu' ]

cppkeywords = [  'alignas'
               , 'alignof'
               , 'and'
               , 'and_eq'
               , 'asm'
               , 'auto'
               , 'bitand'
               , 'bitor'
               , 'bool'
               , 'break'
               , 'case'
               , 'catch'
               , 'char'
               , 'char16_t'
               , 'char32_t'
               , 'class'
               , 'compl'
               , 'concept'
               , 'const'
               , 'constexpr'
               , 'const_cast'
               , 'continue'
               , 'decltype'
               , 'default'
               , 'define'
               , 'delete'
               , 'do'
               , 'double'
               , 'dynamic_cast'
               , 'else'
               , 'elif'
               , 'endif'
               , 'enum'
               , 'explicit'
               , 'export'
               , 'extern'
               , 'false'
               , 'float'
               , 'for'
               , 'friend'
               , 'goto'
               , 'if'
               , 'ifdef'
               , 'ifndef'
               , 'inline'
               , 'int'
               , 'long'
               , 'mutable'
               , 'namespace'
               , 'new'
               , 'noexcept'
               , 'noreturn'
               , 'not'
               , 'not_eq'
               , 'nullptr'
               , 'operator'
               , 'or'
               , 'or_eq'
               , 'private'
               , 'protected'
               , 'public'
               , 'register'
               , 'reinterpret_cast'
               , 'requires'
               , 'return'
               , 'short'
               , 'signed'
               , 'sizeof'
               , 'static'
               , 'static_assert'
               , 'static_cast'
               , 'struct'
               , 'switch'
               , 'template'
               , 'this'
               , 'thread_local'
               , 'throw'
               , 'true'
               , 'try'
               , 'typedef'
               , 'typeid'
               , 'typename'
               , 'union'
               , 'unsigned'
               , 'using'
               , 'virtual'
               , 'void'
               , 'volatile'
               , 'wchar'
               , 'wchar_t'
               , 'while'
               , 'xor'
               , 'xor_eq'
               , 'declspec'
               ]

stdlibwords = [  'std'
               , 'alloc'
               , 'argc'
               , 'argv'
               , 'atexit'
               , 'bufsiz'
               , 'cbegin'
               , 'cend'
               , 'chrono'
               , 'cmath'
               , 'codecvt'
               , 'cplusplus'
               , 'cref'
               , 'cstdint'
               , 'cstdio'
               , 'cstdlib'
               , 'cstring'
               , 'ctime'
               , 'ctype'
               , 'cuchar'
               , 'cxxabi'
               , 'declval'
               , 'errno'
               , 'fclose'
               , 'fflush'
               , 'fopen'
               , 'foreach'
               , 'fprintf'
               , 'fread'
               , 'ftime'
               , 'fwrite'
               , 'fseek'
               , 'ftell'
               , 'getenv'
               , 'getcwd'
               , 'gettimeofday'
               , 'glibcpp'
               , 'glibcxx'
               , 'gnuc'
               , 'iomanip'
               , 'iostreams'
               , 'libcpp'
               , 'localtime'
               , 'mbsinit'
               , 'mbstate'
               , 'mbstowcs'
               , 'mbtowc'
               , 'memcmp'
               , 'memcpy'
               , 'memset'
               , 'mutex'
               , 'nanosleep'
               , 'npos'
               , 'ostream'
               , 'printf'
               , 'putenv'
               , 'rbegin'
               , 'seekg'
               , 'setbase'
               , 'setbuf'
               , 'setlocale'
               , 'setprecision'
               , 'setvbuf'
               , 'snprintf'
               , 'stdarg'
               , 'stderr'
               , 'stdio'
               , 'stringstream'
               , 'stdlib'
               , 'stdout'
               , 'strcasecmp'
               , 'strchr'
               , 'strcmp'
               , 'stricmp'
               , 'strncpy'
               , 'strnlen'
               , 'strrchr'
               , 'strstr'
               , 'strstream'
               , 'strtok'
               , 'strtol'
               , 'tellg'
               , 'timeb'
               , 'toupper'
               , 'towupper'
               , 'typeinfo'
               , 'typeindex'
               , 'uintptr'
               , 'uintptr_t'
               , 'unistd'
               , 'uchar'
               , 'vscprintf'
               , 'vsnprintf'
               , 'vsnwprintf'
               , 'vsprintf'
               , 'vswprintf'
               , 'wcscasecmp'
               , 'wcscmp'
               , 'wcsicmp'
               , 'wcslen'
               , 'wcstombs'
               , 'wcsstr'
               , 'wctype'
               , 'wmain'
               , 'wstring'
               ]

win32keywords = [ 'windows'
                , 'afx'
                , 'cpprtti'
                , 'crtdbg'
                , 'dbghelp'
                , 'hmodule'
                , 'hresult'
                , 'msvc'
                , 'wsacleanup'
                , 'wsadata'
                , 'wsaget'
                , 'wsastartup'
                ]

csharpkeywords = [  'abstract'
                  , 'as'
                  , 'base'
                  , 'bool'
                  , 'break'
                  , 'byte'
                  , 'case'
                  , 'catch'
                  , 'char'
                  , 'checked'
                  , 'class'
                  , 'const'
                  , 'continue'
                  , 'decimal'
                  , 'default'
                  , 'delegate'
                  , 'do'
                  , 'double'
                  , 'else'
                  , 'enum'
                  , 'event'
                  , 'explicit'
                  , 'extern'
                  , 'false'
                  , 'finally'
                  , 'float'
                  , 'for'
                  , 'foreach'
                  , 'goto'
                  , 'if'
                  , 'implicit'
                  , 'in'
                  , 'int'
                  , 'interface'
                  , 'internal'
                  , 'is'
                  , 'lock'
                  , 'long'
                  , 'namespace'
                  , 'new'
                  , 'null'
                  , 'object'
                  , 'operator'
                  , 'out'
                  , 'override'
                  , 'params'
                  , 'private'
                  , 'protected'
                  , 'public'
                  , 'readonly'
                  , 'ref'
                  , 'return'
                  , 'sbyte'
                  , 'sealed'
                  , 'short'
                  , 'sizeof'
                  , 'stackalloc'
                  , 'static'
                  , 'string'
                  , 'struct'
                  , 'switch'
                  , 'this'
                  , 'throw'
                  , 'true'
                  , 'try'
                  , 'typeof'
                  , 'uint'
                  , 'ulong'
                  , 'unchecked'
                  , 'unsafe'
                  , 'ushort'
                  , 'using'
                  , 'virtual'
                  , 'void'
                  , 'volatile'
                  , 'while'
                  ]

csharpwords = [  'int'
               , 'uint'
               , 'long'
               , 'ulong'
               , 'var'
               ]

cppext = [ '.c', '.cpp', '.cxx', '.cc', '.h', '.hpp', '.hxx', '.ipp' ]
csext = [ '.cs' ]


def appendix(d):
    for word in d:
        if '_' in word:
            d.append(word.replace('_', ''))


def getkeywords(file):
    langkeywords = []
    root, ext = os.path.splitext(file)
    if ext in cppext:
        langkeywords.extend(cppkeywords)
        langkeywords.extend(cppwords)
        langkeywords.extend(stdlibwords)
        langkeywords.extend(win32keywords)
        langkeywords.extend(foramtwords)
    elif ext in csext:
        langkeywords.extend(csharpkeywords)
        langkeywords.extend(csharpwords)
    appendix(langkeywords)
    return langkeywords
