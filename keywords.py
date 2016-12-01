import os

programwords =  [ 'cygwin'
                , 'cpplint'
                , 'cuda'
                , 'csv'
                , 'doxygen'
                , 'freebsd'
                , 'http'
                , 'https'
                , 'iphone'
                , 'jis'
                , 'junit'
                , 'linux'
                , 'microsoft'
                , 'mingw'
                , 'mwerks'
                , 'nacl'
                , 'posix'
                , 'ppapi'
                , 'shiftjis'
                , 'solaris'
                , 'sunos'
                , 'unicode'
                , 'utf'
                , 'wandbox'
                , 'xterm'
                ]

cppwords = [  'cpp'
            , '_bsd_source'
            , '_xopen_source'
            , 'cxx'
            , 'hpp'
            , 'ipp'
            , 'uint'
            , 'ulong'
            , 'armcc'
            , 'borlandc'
            , 'cudacc'
            , 'gcc'
            , 'gunc'
            , 'ibmcpp'
            , 'rtti'
            , 'sfinae'
            , 'stlport'
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
               , 'include'
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
               , 'pragma'
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
               , '__cxa_demangle'
               , '_mkdir'
               , 'abi'
               , 'addrinfo'
               , 'ai_addrlen'
               , 'algorithm'
               , 'alloc'
               , 'arg'
               , 'argc'
               , 'argv'
               , 'arpa'
               , 'atexit'
               , 'bufsiz'
               , 'cbegin'
               , 'cend'
               , 'chrono'
               , 'cin'
               , 'closesocket'
               , 'cmath'
               , 'codecvt'
               , 'copyfmt'
               , 'cout'
               , 'cplusplus'
               , 'crbegin'
               , 'cref'
               , 'crend'
               , 'cstdint'
               , 'cstdio'
               , 'cstdlib'
               , 'cstring'
               , 'ctime'
               , 'ctype'
               , 'cuchar'
               , 'cxxabi'
               , 'declval'
               , 'eoverflow'
               , 'endl'
               , 'errno'
               , 'fclose'
               , 'fflush'
               , 'fopen'
               , 'foreach'
               , 'fprintf'
               , 'fread'
               , 'freeaddrinfo'
               , 'ftime'
               , 'fwrite'
               , 'fseek'
               , 'ftell'
               , 'hex'
               , 'intmax_t'
               , 'iofbf'
               , 'iostream'
               , 'istringstream'
               , 'getaddrinfo'
               , 'getenv'
               , 'getcwd'
               , 'getpid'
               , 'gettimeofday'
               , 'glibcpp'
               , 'glibcxx'
               , 'gnuc'
               , 'iomanip'
               , 'iostreams'
               , 'iter_swap'
               , 'libcpp'
               , 'localtime'
               , 'mbsinit'
               , 'mbstate'
               , 'mbstowcs'
               , 'mbtowc'
               , 'memcmp'
               , 'memcpy'
               , 'memmove'
               , 'memset'
               , 'mutex'
               , 'nanosleep'
               , 'netdb'
               , 'nothrow'
               , 'npos'
               , 'numeric_limits'
               , 'ostream'
               , 'printf'
               , 'putenv'
               , 'rbegin'
               , 'readlink'
               , 'regex'
               , 'rend'
               , 'seekg'
               , 'setbase'
               , 'setbuf'
               , 'setenv'
               , 'setfill'
               , 'setlocale'
               , 'setprecision'
               , 'setw'
               , 'setvbuf'
               , 'snprintf'
               , 'sockaddr_in'
               , 'sprintf'
               , 'ssize_t'
               , 'sstream'
               , 'stdarg'
               , 'stderr'
               , 'stdio'
               , 'stdexcept'
               , 'stringstream'
               , 'stdlib'
               , 'stdout'
               , 'strcasecmp'
               , 'strcat'
               , 'strchr'
               , 'strcmp'
               , 'strcmpi'
               , 'strcpy'
               , 'strdup'
               , 'streambuf'
               , 'strerror'
               , 'stricmp'
               , 'strlen'
               , 'strlwr'
               , 'strncmp'
               , 'strncpy'
               , 'strnicmp'
               , 'strnlen'
               , 'strrchr'
               , 'strset'
               , 'strstr'
               , 'strstream'
               , 'strtok'
               , 'strtol'
               , 'strtombs'
               , 'strtoul'
               , 'strupr'
               , 'substr'
               , 'swprintf'
               , 'sysctl'
               , 'tellg'
               , 'timeb'
               , 'timespec'
               , 'timeval'
               , 'tm_mday'
               , 'toupper'
               , 'towupper'
               , 'tv_usec'
               , 'typeinfo'
               , 'typeindex'
               , 'uchar'
               , 'uintmax_t'
               , 'uintptr'
               , 'uintptr_t'
               , 'unistd'
               , 'usleep'
               , 'vprintf'
               , 'vscprintf'
               , 'vsnprintf'
               , 'vsnwprintf'
               , 'vsprintf'
               , 'vswprintf'
               , 'wcscasecmp'
               , 'wcscat'
               , 'wcschr'
               , 'wcscmp'
               , 'wcscmpi'
               , 'wcscpy'
               , 'wcsdup'
               , 'wcsicmp'
               , 'wcslen'
               , 'wcslwr'
               , 'wcsncmp'
               , 'wcsncpy'
               , 'wcsnicmp'
               , 'wcsnlen'
               , 'wcsrchr'
               , 'wcsset'
               , 'wcsstr'
               , 'wcstok'
               < 'wcstol'
               , 'wcstombs'
               < 'wcstoul'
               , 'wcsupr'
               , 'wctype'
               , 'wmain'
               , 'wstring'
               , 'xlocnum'
               , 'xtree'
               ]

win32keywords = [ 'windows'
                , '__debugbreak'
                , '_call_reportfault'
                , '_tcscat'
                , '_tcschr'
                , '_tcscpy'
                , '_tcslen'
                , '_tcsncpy'
                , '_tcsrchr'
                , '_tcsstr'
                , '_tcstod'
                , '_tcstol'
                , 'afx'
                , 'countof'
                , 'cpprtti'
                , 'crtdbg'
                , 'dbghelp'
                , 'dll'
                , 'farproc'
                , 'hmenu'
                , 'hmodule'
                , 'hresult'
                , 'lpstr'
                , 'lpwstr'
                , 'msvc'
                , 'pminidump'
                , 'sem_failcriticalerrors'
                , 'sem_noalignmentfaultexcept'
                , 'sem_nogpfaulterrorbox'
                , 'sem_noopenfileerrorbox'
                , 'shlobj'
                , 'shlwapi'
                , 'systemtime'
                , 'winapi'
                , 'winnt'
                , 'wsacleanup'
                , 'wsadata'
                , 'wsaget'
                , 'wsastartup'
                ]

mfckeywords = [ 'mfc'
              , 'carray'
              , 'ccontainer'
              , 'clist'
              , 'cmap'
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
                  , 'linq'
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
objcext = [ '.mm', '.m' ]


def appendix(d):
    for word in d:
        if '_' in str(word):
            d.append(word.replace('_', ''))
            for s in word.split('_'):
                if len(s) > 2 and s not in d:
                    d.append(s)


def make_cppkeywords():
    langkeywords = programwords
    langkeywords.extend(cppkeywords)
    langkeywords.extend(cppwords)
    langkeywords.extend(stdlibwords)
    langkeywords.extend(win32keywords)
    langkeywords.extend(mfckeywords)
    langkeywords.extend(foramtwords)
    appendix(langkeywords)
    return langkeywords


def make_csharpkeywords():
    langkeywords = programwords
    langkeywords.extend(csharpkeywords)
    langkeywords.extend(csharpwords)
    appendix(langkeywords)
    return langkeywords


def make_objckeywords():
    langkeywords = programwords
    langkeywords.extend(cppkeywords)
    langkeywords.extend(cppwords)
    langkeywords.extend(stdlibwords)
    langkeywords.extend(foramtwords)
    appendix(langkeywords)
    return langkeywords


def make_defaultkeywords():
    langkeywords = programwords
    appendix(langkeywords)
    return langkeywords


cppkeywords_all = None
csharpkeywords_all = None
objckeywords_all = None
defaultkeywords_all = None

def getkeywords(file):
    global cppkeywords_all
    global csharpkeywords_all
    global objckeywords_all
    global defaultkeywords_all
    root, ext = os.path.splitext(file)
    if ext in cppext:
        if cppkeywords_all is None:
            cppkeywords_all = make_cppkeywords()
        return cppkeywords_all
    elif ext in csext:
        if csharpkeywords_all is None:
            csharpkeywords_all = make_csharpkeywords()
        return csharpkeywords_all
    elif ext in objcext:
        if objckeywords_all is None:
            objckeywords_all = make_objckeywords()
        return objckeywords_all

    if defaultkeywords_all is None:
        defaultkeywords_all = make_defaultkeywords()
    return defaultkeywords_all
