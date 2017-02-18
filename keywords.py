import os

commonwords =  [ 'alpha'
                , 'beta'
                , 'cygwin'
                , 'cpplint'
                , 'cuda'
                , 'csv'
                , 'dot'
                , 'doxygen'
                , 'endian'
                , 'euc'
                , 'freebsd'
                , 'google'
                , 'http'
                , 'https'
                , 'iphone'
                , 'jis'
                , 'junit'
                , 'linux'
                , 'macro'
                , 'microsoft'
                , 'mingw'
                , 'mono'
                , 'mwerks'
                , 'nacl'
                , 'posix'
                , 'ppapi'
                , 'regex'
                , 'shiftjis'
                , 'solaris'
                , 'sunos'
                , 'unicode'
                , 'url'
                , 'utf'
                , 'wandbox'
                , 'xterm'
                ]

xmlwords = [  'xml'
            , 'xmlattribute'
            , 'xmldata'
            , 'xmldocument'
            , 'xmlelement'
            , 'xmlerror'
            , 'xmlfooter'
            , 'xmlheader'
            , 'xmlprinter'
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
               , 'eof'
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
               , 'undef'
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
               , 'acos'
               , 'acosf'
               , 'acosl'
               , 'addrinfo'
               , 'ai_addrlen'
               , 'algorithm'
               , 'alloc'
               , 'alloca'
               , 'arg'
               , 'argc'
               , 'argv'
               , 'arpa'
               , 'asin'
               , 'asinf'
               , 'asinl'
               , 'asprintf'
               , 'atan'
               , 'atanf'
               , 'atanl'
               , 'atoi'
               , 'atof'
               , 'atol'
               , 'atexit'
               , 'bufsiz'
               , 'calloc'
               , 'cbegin'
               , 'cend'
               , 'cerr'
               , 'chrono'
               , 'cin'
               , 'closesocket'
               , 'cmath'
               , 'codecvt'
               , 'copyfmt'
               , 'cos'
               , 'cosf'
               , 'coshf'
               , 'coshl'
               , 'cosl'
               , 'cout'
               , 'cplusplus'
               , 'crbegin'
               , 'cref'
               , 'crend'
               , 'cstddef'
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
               , 'execl'
               , 'execle'
               , 'execlp'
               , 'execlpe'
               , 'execv'
               , 'execve'
               , 'execvp'
               , 'execvpe'
               , 'fabs'
               , 'fclose'
               , 'fcntl'
               , 'feof'
               , 'ferror'
               , 'fflush'
               , 'fgetc'
               , 'fgetpos'
               , 'fgets'
               , 'fgetwc'
               , 'fgetws'
               , 'fileno'
               , 'fmod'
               , 'fmodf'
               , 'fmodl'
               , 'fopen'
               , 'foreach'
               , 'fprintf'
               , 'fnprintf'
               , 'fputc'
               , 'fputs'
               , 'fputwc'
               , 'fputws'
               , 'fread'
               , 'freeaddrinfo'
               , 'freopen'
               , 'frexp'
               , 'fscanf'
               , 'fseek'
               , 'fseeko'
               , 'fsetpos'
               , 'fstat'
               , 'fstream'
               , 'fsync'
               , 'ftell'
               , 'ftello'
               , 'ftime'
               , 'ftok'
               , 'ftruncate'
               , 'fwrite'
               , 'getaddrinfo'
               , 'getchar'
               , 'getcwd'
               , 'getenv'
               , 'gethostbyaddr'
               , 'gethostbyname'
               , 'getline'
               , 'getnetbyname'
               , 'getpid'
               , 'getprotobyname'
               , 'getpwnam'
               , 'getrlimit'
               , 'getservbyname'
               , 'getservbyport'
               , 'gettimeofday'
               , 'glibc'
               , 'glibcpp'
               , 'glibcxx'
               , 'gmtime'
               , 'gnuc'
               , 'hex'
               , 'ifstream'
               , 'intmax_t'
               , 'iofbf'
               , 'iostream'
               , 'iomanip'
               , 'iostreams'
               , 'intptr_t'
               , 'inttypes'
               , 'isalnum'
               , 'isalpha'
               , 'isatty'
               , 'isblank'
               , 'iscntrl'
               , 'isdigit'
               , 'isgraph'
               , 'islower'
               , 'isprint'
               , 'ispunct'
               , 'isspace'
               , 'istringstream'
               , 'isupper'
               , 'isxdigit'
               , 'iter_swap'
               , 'itoa'
               , 'libcpp'
               , 'localtime'
               , 'log'
               , 'logf'
               , 'logl'
               , 'lseek'
               , 'lstat'
               , 'mblen'
               , 'mbsinit'
               , 'mbstate'
               , 'mbstowcs'
               , 'mbtowc'
               , 'memchr'
               , 'memcmp'
               , 'memcpy'
               , 'memmove'
               , 'memset'
               , 'minmax'
               , 'mktime'
               , 'modf'
               , 'mutex'
               , 'nanosleep'
               , 'netdb'
               , 'nothrow'
               , 'npos'
               , 'numeric_limits'
               , 'ofstream'
               , 'ostream'
               , 'ostringstream'
               , 'printf'
               , 'pthread'
               , 'ptrdiff_t'
               , 'putenv'
               , 'rbegin'
               , 'rdbuf'
               , 'readlink'
               , 'regex'
               , 'rend'
               , 'rfind'
               , 'rmdir'
               , 'scanf'
               , 'seekg'
               , 'setbase'
               , 'setbuf'
               , 'setegid'
               , 'seteuid'
               , 'setenv'
               , 'setfill'
               , 'setjmp'
               , 'setlocale'
               , 'setp'
               , 'setprecision'
               , 'setrlimit'
               , 'setuid'
               , 'setw'
               , 'setvbuf'
               , 'sin'
               , 'sinf'
               , 'sinh'
               , 'sinhf'
               , 'sinhl'
               , 'sinl'
               , 'snprintf'
               , 'snwprintf'
               , 'sockaddr_in'
               , 'sprintf'
               , 'sputc'
               , 'sqrt'
               , 'sqrtf'
               , 'sqrtl'
               , 'sscanf'
               , 'ssize_t'
               , 'sstream'
               , 'stat'
               , 'stdarg'
               , 'stdbool'
               , 'stderr'
               , 'stdexcept'
               , 'stdint'
               , 'stdio'
               , 'stdlib'
               , 'stdout'
               , 'strcasecmp'
               , 'strcat'
               , 'strchr'
               , 'strcmp'
               , 'strcmpi'
               , 'strcoll'
               , 'strcpy'
               , 'strcspn'
               , 'strdup'
               , 'strdupa'
               , 'streambuf'
               , 'strerror'
               , 'strftime'
               , 'stricmp'
               , 'stringstream'
               , 'strlen'
               , 'strlwr'
               , 'strncasecmp'
               , 'strncat'
               , 'strncmp'
               , 'strncpy'
               , 'strndup'
               , 'strndupa'
               , 'strnicmp'
               , 'strnlen'
               , 'strrchr'
               , 'strset'
               , 'strspn'
               , 'strstr'
               , 'strstream'
               , 'strtod'
               , 'strtof'
               , 'strtok'
               , 'strtol'
               , 'strtold'
               , 'strtoll'
               , 'strtombs'
               , 'strtoul'
               , 'strupr'
               , 'substr'
               , 'swscanf'
               , 'swprintf'
               , 'symlink'
               , 'sysctl'
               , 'tellg'
               , 'timeb'
               , 'timespec'
               , 'timeval'
               , 'tm_mday'
               , 'tolower'
               , 'towlower'
               , 'toupper'
               , 'towupper'
               , 'tv_usec'
               , 'typeinfo'
               , 'typeindex'
               , 'uchar'
               , 'uintmax_t'
               , 'uintptr'
               , 'uintptr_t'
               , 'ungetc'
               , 'ungetwc'
               , 'unistd'
               , 'usleep'
               , 'utime'
               , 'vasprintf'
               , 'vfnprintf'
               , 'vfprintf'
               , 'vfree'
               , 'vfscanf'
               , 'vfwprintf'
               , 'vmalloc'
               , 'vprintf'
               , 'vscanf'
               , 'vscprintf'
               , 'vsnprintf'
               , 'vsnwprintf'
               , 'vsprintf'
               , 'vsscanf'
               , 'vswprintf'
               , 'vwprintf'
               , 'wcscasecmp'
               , 'wcscat'
               , 'wcschr'
               , 'wcscmp'
               , 'wcscmpi'
               , 'wcscoll'
               , 'wcscpy'
               , 'wcscspn'
               , 'wcsdup'
               , 'wcsdupa'
               , 'wcsftime'
               , 'wcsicmp'
               , 'wcslen'
               , 'wcslwr'
               , 'wcsncasecmp'
               , 'wcsncat'
               , 'wcsncmp'
               , 'wcsncpy'
               , 'wcsndup'
               , 'wcsndupa'
               , 'wcsnicmp'
               , 'wcsnlen'
               , 'wcsrchr'
               , 'wcsset'
               , 'wcsspn'
               , 'wcsstr'
               , 'wcstod'
               , 'wcstof'
               , 'wcstok'
               < 'wcstol'
               < 'wcstold'
               < 'wcstoll'
               , 'wcstombs'
               < 'wcstoul'
               < 'wcstoull'
               , 'wcsupr'
               , 'wctype'
               , 'wistringstream'
               , 'wmain'
               , 'wprintf'
               , 'wscanf'
               , 'wstreambuf'
               , 'wstring'
               , 'wstringstream'
               , 'xlocnum'
               , 'xtree'
               ]

predefines = [    '__SUNPRO_CC'
                , '__SYMBIAN__'
                ]

win32keywords = [ 'windows'
                , '__debugbreak'
                , '__forceinline'
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
                , '_tmain'
                , '_tprintf'
                , '_wfopen_s'
                , 'afx'
                , 'afxdll'
                , 'countof'
                , 'cpprtti'
                , 'crtdbg'
                , 'dbghelp'
                , 'dll'
                , 'dllexport'
                , 'dllimport'
                , 'farproc'
                , 'hbitmap'
                , 'hbrush'
                , 'hcursor'
                , 'hdc'
                , 'hdrop'
                , 'henhmetafile'
                , 'hfile'
                , 'hfont'
                , 'hgdiobj'
                , 'hglobal'
                , 'hhook'
                , 'hicon'
                , 'hinstance'
                , 'hkey'
                , 'hlocal'
                , 'hmenu'
                , 'hmetafile'
                , 'hmonitor'
                , 'hmodule'
                , 'hpalette'
                , 'hpen'
                , 'hresult'
                , 'hrgn'
                , 'hrsrc'
                , 'hwnd'
                , 'lpbool'
                , 'lpbyte'
                , 'lpcolorref'
                , 'lpcstr'
                , 'lpctstr'
                , 'lpcwstr'
                , 'lpdword'
                , 'lpint'
                , 'lplong'
                , 'lpstr'
                , 'lptstr'
                , 'lpvoid'
                , 'lpword'
                , 'lpwstr'
                , 'lresult'
                , 'mmresult'
                , 'msvc'
                , 'ndebug'
                , 'pminidump'
                , 'sem_failcriticalerrors'
                , 'sem_noalignmentfaultexcept'
                , 'sem_nogpfaulterrorbox'
                , 'sem_noopenfileerrorbox'
                , 'shlobj'
                , 'shlwapi'
                , 'systemtime'
                , 'tchar'
                , 'tcin'
                , 'tcout'
                , 'winapi'
                , 'winapifamily'
                , 'winnt'
                , 'wopen'
                , 'wsacleanup'
                , 'wsadata'
                , 'wsaget'
                , 'wsastartup'
                , 'wsprintf'
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
                  , 'substring'
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
               , 'ienumerator'
               , 'ioexception'
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
    langkeywords = commonwords
    langkeywords.extend(cppkeywords)
    langkeywords.extend(cppwords)
    langkeywords.extend([ s.lower() for s in predefines ])
    langkeywords.extend(stdlibwords)
    langkeywords.extend(win32keywords)
    langkeywords.extend(mfckeywords)
    langkeywords.extend(foramtwords)
    langkeywords.extend(xmlwords)
    appendix(langkeywords)
    return langkeywords


def make_csharpkeywords():
    langkeywords = commonwords
    langkeywords.extend(csharpkeywords)
    langkeywords.extend(csharpwords)
    appendix(langkeywords)
    return langkeywords


def make_objckeywords():
    langkeywords = commonwords
    langkeywords.extend(cppkeywords)
    langkeywords.extend(cppwords)
    langkeywords.extend(stdlibwords)
    langkeywords.extend(foramtwords)
    appendix(langkeywords)
    return langkeywords


def make_defaultkeywords():
    langkeywords = commonwords
    appendix(langkeywords)
    return langkeywords


cppkeywords_all = None
csharpkeywords_all = None
objckeywords_all = None
defaultkeywords_all = None

def getlanguage(file):
    root, ext = os.path.splitext(file)
    if ext in cppext:
        return 'c++'
    elif ext in csext:
        return 'c#'
    elif ext in objcext:
        return 'obj-c'
    return None


def getkeywords_from_ext(ext):
    global cppkeywords_all
    global csharpkeywords_all
    global objckeywords_all
    global defaultkeywords_all
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


def getkeywords(file):
    root, ext = os.path.splitext(file)
    return getkeywords_from_ext(ext)
