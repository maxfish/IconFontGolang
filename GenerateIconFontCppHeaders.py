# Convert Font Awesome, Fork Awesome, Google Material Design, Kenney Game and Fontaudio
# icon font parameters to C, C++, C# and Go compatible formats.
#
#------------------------------------------------------------------------------
# 1 - Source material
#
#   1.1 - Font Awesome
#       1.1.1 - version 4
#           https://raw.githubusercontent.com/FortAwesome/Font-Awesome/fa-4/src/icons.yml
#           https://github.com/FortAwesome/Font-Awesome/blob/fa-4/fonts/fontawesome-webfont.ttf
#       1.1.2 - version 5
#           https://raw.githubusercontent.com/FortAwesome/Font-Awesome/master/metadata/icons.yml
#           https://github.com/FortAwesome/Font-Awesome/blob/master/webfonts/fa-brands-400.ttf
#           https://github.com/FortAwesome/Font-Awesome/blob/master/webfonts/fa-regular-400.ttf
#           https://github.com/FortAwesome/Font-Awesome/blob/master/webfonts/fa-solid-900.ttf
#       1.1.3 - version 5 Pro
#           Download files from https://fontawesome.com
#           \fontawesome-pro-n.n.n-web\metadata\icons.yml
#           \fontawesome-pro-n.n.n-web\webfonts\fa-brands-400.ttf
#           \fontawesome-pro-n.n.n-web\webfonts\fa-light-300.ttf
#           \fontawesome-pro-n.n.n-web\webfonts\fa-regular-400.ttf
#           \fontawesome-pro-n.n.n-web\webfonts\fa-solid-900.ttf
#   1.2 - Fork Awesome
#           https://raw.githubusercontent.com/ForkAwesome/Fork-Awesome/master/src/icons/icons.yml
#           https://github.com/ForkAwesome/Fork-Awesome/blob/master/fonts/forkawesome-webfont.ttf
#   1.3 - Google Material Design
#           https://raw.githubusercontent.com/google/material-design-icons/master/iconfont/codepoints
#           https://github.com/google/material-design-icons/blob/master/iconfont/MaterialIcons-Regular.ttf
#   1.4 - Kenney Game icons
#           https://raw.githubusercontent.com/nicodinh/kenney-icon-font/master/css/kenney-icons.css
#           https://github.com/nicodinh/kenney-icon-font/blob/master/fonts/kenney-icon-font.ttf
#   1.5 - Fontaudio
#           https://raw.githubusercontent.com/fefanto/fontaudio/master/font/fontaudio.css
#           https://github.com/fefanto/fontaudio/blob/master/font/fontaudio.ttf
#------------------------------------------------------------------------------
# 2 - Data sample
#
#   Font Awesome example:
#           - input:            music:
#                                 changes:
#                                   - '1'
#                                   - 5.0.0
#                                 label: Music
#                                 search:
#                                   terms:
#                                     - note
#                                     - sound
#                                 styles:
#                                   - solid
#                                 unicode: f001
#           - output C and C++:     #define ICON_FA_MUSIC "\xef\x80\x81"	// U+f001
#           - output C#:            public const string Music = "\uf001";
#
#   All fonts have computed min and max unicode fonts ICON_MIN and ICON_MAX
#           - output C and C++:     #define ICON_MIN_FA 0xf000
#                                   #define ICON_MAX_FA 0xf2e0
#               Exception for Font Awesome brands: we use ICON_MIN_FAB and ICON_MAX_FAB
#               to differentiate between brand and non-brand icons so they can be used together
#               (the defines must be unique in C and C++).
#           - output C#:            public const int IconMin = 0xf000;
#                                   public const int IconMax = 0xf2e0;
#
#------------------------------------------------------------------------------
# 3 - Script dependencies
#
#   3.1 - Fonts source material online
#   3.2 - Python 3 - https://www.python.org/downloads/
#   3.3 - Requests - https://pypi.org/project/requests/
#   3.4 - PyYAML - https://pypi.org/project/PyYAML/
#
#------------------------------------------------------------------------------
# 4 - References
#
#   GitHub repository: https://github.com/juliettef/IconFontCppHeaders/
#
#------------------------------------------------------------------------------


import requests
import yaml
import os
import sys

if sys.version_info[0] < 3:
    raise Exception( "Python 3 or a more recent version is required." )

# Fonts

class Font:
    font_name = '[ ERROR - missing font name ]'
    font_abbr = '[ ERROR - missing font abbreviation ]'
    font_minmax_abbr = ''   # optional - use if min and max defines must be differentiated. See Font Awesome Brand for example.
    font_data = '[ ERROR - missing font data file or url ]'
    ttfs = '[ ERROR - missing ttf ]'

    @classmethod
    def get_icons( cls, input_data ):
        # intermediate representation of the fonts data, identify the min and max
        print( '[ ERROR - missing implementation of class method get_icons for {!s} ]'.format( cls.font_name ))
        icons_data = {}
        icons_data.update({ 'font_min' : '[ ERROR - missing font min ]',
                            'font_max' : '[ ERROR - missing font max ]',
                            'icons' : '[ ERROR - missing list of pairs [ font icon name, code ]]' })
        return icons_data

    @classmethod
    def get_intermediate_representation( cls ):
        font_ir = {}
        if 'http' in cls.font_data:  # if url, download data
            response = requests.get( cls.font_data, timeout = 2 )
            if response.status_code == 200:
                input_raw = response.text
                print( 'Downloaded - ' + cls.font_name )
            else:
                raise Exception( 'Download failed - ' + cls.font_name )
        else:   # read data from file if present
            if os.path.isfile( cls.font_data ):
                with open( cls.font_data, 'r' ) as f:
                    input_raw = f.read()
                    f.close()
                    print( 'File read - ' + cls.font_name )
            else:
                raise Exception( 'File ' + cls.font_name + ' missing - ' + cls.font_data )
        if input_raw:
            icons_data = cls.get_icons( input_raw )
            font_ir.update( icons_data )
            font_ir.update({ 'font_data' : cls.font_data,
                             'font_name' : cls.font_name,
                             'font_abbr' : cls.font_abbr,
                             'font_minmax_abbr' : cls.font_minmax_abbr,
                             'ttfs' : cls.ttfs, })
            print( 'Generated intermediate data - ' + cls.font_name )
        return font_ir


class FontFA4( Font ):              # legacy Font Awesome version 4
    font_name = 'Font Awesome 4'
    font_abbr = 'FA'
    font_data = 'https://raw.githubusercontent.com/FortAwesome/Font-Awesome/fa-4/src/icons.yml'
    ttfs = [[ font_abbr, 'fontawesome-webfont.ttf', 'https://github.com/FortAwesome/Font-Awesome/blob/fa-4/fonts/fontawesome-webfont.ttf' ]]

    @classmethod
    def get_icons( cls, input_data ):
        icons_data = { }
        data = yaml.safe_load( input_data )
        font_min = 'ffff'
        font_max = '0'
        icons = []
        for item in data[ 'icons' ]:
            if item[ 'unicode' ] < font_min:
                font_min = item[ 'unicode' ]
            if item[ 'unicode' ] >= font_max:
                font_max = item[ 'unicode' ]
            icons.append([ item[ 'id' ], item[ 'unicode' ]])
        icons_data.update({ 'font_min' : font_min,
                        'font_max' : font_max,
                        'icons' : icons })
        return icons_data


class FontFK( FontFA4 ):            # Fork Awesome, based on Font Awesome 4
    font_name = 'Fork Awesome'
    font_abbr = 'FK'
    font_data = 'https://raw.githubusercontent.com/ForkAwesome/Fork-Awesome/master/src/icons/icons.yml'
    ttfs = [[ font_abbr, 'forkawesome-webfont.ttf', 'https://github.com/ForkAwesome/Fork-Awesome/blob/master/fonts/forkawesome-webfont.ttf' ]]


class FontFA5( Font ):              # Font Awesome version 5 - Regular and Solid styles
    font_name = 'Font Awesome 5'
    font_abbr = 'FA'
    font_data = 'https://raw.githubusercontent.com/FortAwesome/Font-Awesome/master/metadata/icons.yml'
    ttfs = [[ 'FAR', 'fa-regular-400.ttf', 'https://github.com/FortAwesome/Font-Awesome/blob/master/webfonts/fa-regular-400.ttf' ],
            [ 'FAS', 'fa-solid-900.ttf', 'https://github.com/FortAwesome/Font-Awesome/blob/master/webfonts/fa-solid-900.ttf' ]]
    font_fa_style = [ 'regular', 'solid' ]

    @classmethod
    def get_icons( cls, input_data ):
        icons_data = { }
        data = yaml.safe_load( input_data )
        if data:
            font_min = 'ffff'
            font_max = '0'
            icons = []
            for key in data:
                item = data[ key ]
                for style in item[ 'styles' ]:
                    if style in cls.font_fa_style:
                        if [ key, item[ 'unicode' ]] not in icons:
                            if item[ 'unicode' ] < font_min:
                                font_min = item[ 'unicode' ]
                            if item[ 'unicode' ] >= font_max:
                                font_max = item[ 'unicode' ]
                            icons.append([ key, item[ 'unicode' ]])
            icons_data.update({ 'font_min':font_min, 'font_max':font_max, 'icons':icons })
        return icons_data


class FontFA5Brands( FontFA5 ):     # Font Awesome version 5 - Brand style
    font_name = 'Font Awesome 5 Brands'
    font_minmax_abbr = 'FAB'
    ttfs = [[ 'FAB', 'fa-brands-400.ttf', 'https://github.com/FortAwesome/Font-Awesome/blob/master/webfonts/fa-brands-400.ttf' ]]
    font_fa_style = [ 'brands' ]


class FontFA5Pro( FontFA5 ):        # Font Awesome version 5 Pro - Light, Regular and Solid styles
    font_name = 'Font Awesome 5 Pro'
    font_data = 'icons.yml'
    ttfs = [[ 'FAL', 'fa-light-300.ttf', 'fa-light-300.ttf' ],
            [ 'FAR', 'fa-regular-400.ttf', 'fa-regular-400.ttf' ],
            [ 'FAS', 'fa-solid-900.ttf', 'fa-solid-900.ttf' ]]
    font_fa_style = [ 'light', 'regular', 'solid' ]


class FontFA5ProBrands( FontFA5 ):  # Font Awesome version 5 Pro - Brand style
    font_name = 'Font Awesome 5 Pro Brands'
    font_minmax_abbr = 'FAB'
    font_data = 'icons.yml'
    ttfs = [[ 'FAB', 'fa-brands-400.ttf', 'fa-brands-400.ttf' ]]
    font_fa_style = [ 'brands' ]


class FontMD( Font ):               # Material Design
    font_name = 'Material Design'
    font_abbr = 'MD'
    font_data = 'https://raw.githubusercontent.com/google/material-design-icons/master/iconfont/codepoints'
    ttfs = [[ font_abbr, 'MaterialIcons-Regular.ttf', 'https://github.com/google/material-design-icons/blob/master/iconfont/MaterialIcons-Regular.ttf' ]]

    @classmethod
    def get_icons( cls, input_data ):
        icons_data = {}
        lines = str.split( input_data, '\n' )
        if lines:
            font_min = 'ffff'
            font_max = '0'
            icons = []
            for line in lines :
                words = str.split(line)
                if words and len( words ) >= 2:
                    if words[ 1 ] < font_min:
                        font_min = words[ 1 ]
                    if words[ 1 ] >= font_max:
                        font_max = words[ 1 ]
                    icons.append( words )
            icons_data.update({ 'font_min' : font_min,
                                'font_max' : font_max,
                                'icons' : icons })
        return icons_data


class FontKI( Font ):               # Kenney Game icons
    font_name = 'Kenney'
    font_abbr = 'KI'
    font_data = 'https://raw.githubusercontent.com/nicodinh/kenney-icon-font/master/css/kenney-icons.css'
    ttfs = [[ font_abbr, 'kenney-icon-font.ttf', 'https://github.com/nicodinh/kenney-icon-font/blob/master/fonts/kenney-icon-font.ttf' ]]

    @classmethod
    def get_icons( cls, input_data ):
        icons_data = {}
        lines = str.split( input_data, '\n' )
        if lines:
            font_min = 'ffff'
            font_max = '0'
            icons = []
            for line in lines :
                if '.ki-' in line:
                    words = str.split(line)
                    if words and '.ki-' in words[ 0 ]:
                        font_id = words[ 0 ].partition( '.ki-' )[ 2 ].partition( ':before' )[ 0 ]
                        font_code = words[ 2 ].partition( '"\\' )[ 2 ].partition( '";' )[ 0 ]
                        if font_code < font_min:
                            font_min = font_code
                        if font_code >= font_max:
                            font_max = font_code
                        icons.append([ font_id, font_code ])
            icons_data.update({ 'font_min' : font_min,
                                'font_max' : font_max,
                                'icons' : icons  })
        return icons_data


class FontFAD( Font ):               # Fontaudio
    font_name = 'Fontaudio'
    font_abbr = 'FAD'
    font_data = 'https://raw.githubusercontent.com/fefanto/fontaudio/master/font/fontaudio.css'
    ttfs = [[ font_abbr, 'fontaudio.ttf', 'https://github.com/fefanto/fontaudio/blob/master/font/fontaudio.ttf' ]]

    @classmethod
    def get_icons( cls, input_data ):
        icons_data = {}
        lines = str.split( input_data, '}\n' )
        if lines:
            font_min = 'ffff'
            font_max = '0'
            icons = []
            for line in lines :
                if '.icon-fad-' in line:
                    words = str.split( line )
                    if words and '.icon-fad-' in words[ 0 ]:
                        font_id = words[ 0 ].partition( '.icon-fad-' )[ 2 ].partition( ':before' )[ 0 ]
                        font_code = words[ 3 ].partition( '"\\' )[ 2 ].partition( '";' )[ 0 ]
                        if font_code < font_min:
                            font_min = font_code
                        if font_code >= font_max:
                            font_max = font_code
                        icons.append([ font_id, font_code ])
            icons_data.update({ 'font_min' : font_min,
                                'font_max' : font_max,
                                'icons' : icons  })
        return icons_data


# Languages


class Language:
    language_name = '[ ERROR - missing language name ]'
    file_name = '[ ERROR - missing file name ]'
    intermediate = {}

    def __init__( self, intermediate ):
        self.intermediate = intermediate

    @classmethod
    def prelude( cls ):
        print( '[ ERROR - missing implementation of class method prelude for {!s} ]'.format( cls.language_name ))
        result = '[ ERROR - missing prelude ]'
        return result

    @classmethod
    def lines_minmax( cls ):
        print( '[ ERROR - missing implementation of class method lines_minmax for {!s} ]'.format( cls.language_name ))
        result = '[ ERROR - missing min and max ]'
        return result

    @classmethod
    def line_icon( cls, icon ):
        print( '[ ERROR - missing implementation of class method line_icon for {!s} ]'.format( cls.language_name ))
        result = '[ ERROR - missing icon line ]'
        return result

    @classmethod
    def epilogue( cls ):
        return ''

    @classmethod
    def convert( cls ):
        result = cls.prelude() + cls.lines_minmax()
        for icon in cls.intermediate.get( 'icons' ):
            line_icon = cls.line_icon( icon )
            result += line_icon
        result += cls.epilogue()
        print( 'Converted - {!s} for {!s}'.format( cls.intermediate.get( 'font_name' ), cls.language_name ))
        return result

    @classmethod
    def save_to_file( cls ):
        filename = cls.file_name.format( name = str( cls.intermediate.get( 'font_name' )).replace( ' ', '' ))
        converted = cls.convert()
        with open( filename, 'w' ) as f:
            f.write( converted )
            f.close()
        print( 'Saved - {!s}'.format( filename ))


class LanguageC( Language ):
    language_name = 'C and C++'
    file_name = 'Icons{name}.h'

    @classmethod
    def prelude( cls ):
        tmpl_prelude = '// Generated by https://github.com/juliettef/IconFontCppHeaders script GenerateIconFontCppHeaders.py for languages {lang}\n' + \
            '// from {font_data}\n' + \
            '// for use with {ttf_files}\n' + \
            '#pragma once\n\n'
        ttf_files = []
        for ttf in cls.intermediate.get( 'ttfs' ):
            ttf_files.append( ttf[ 2 ])
        result = tmpl_prelude.format( lang = cls.language_name,
                                      font_data = cls.intermediate.get( 'font_data' ),
                                      ttf_files = ', '.join( ttf_files ))
        tmpl_prelude_define_file_name = '#define FONT_ICON_FILE_NAME_{font_abbr} "{file_name_ttf}"\n'
        for ttf in cls.intermediate.get( 'ttfs' ):
            result += tmpl_prelude_define_file_name.format( font_abbr = ttf[ 0 ], file_name_ttf = ttf[ 1 ])
        return result + '\n'

    @classmethod
    def lines_minmax( cls ):
        tmpl_line_minmax = '#define ICON_{minmax}_{abbr} 0x{val}\n'
        result = tmpl_line_minmax.format( minmax = 'MIN',
                                          abbr = cls.intermediate.get( 'font_minmax_abbr' ) if cls.intermediate.get( 'font_minmax_abbr' ) else cls.intermediate.get('font_abbr'),
                                          val = cls.intermediate.get( 'font_min' )) + \
                 tmpl_line_minmax.format( minmax = 'MAX',
                                          abbr = cls.intermediate.get( 'font_minmax_abbr' ) if cls.intermediate.get( 'font_minmax_abbr' ) else cls.intermediate.get('font_abbr'),
                                          val = cls.intermediate.get( 'font_max' ))
        return result

    @classmethod
    def line_icon( cls, icon ):
        tmpl_line_icon = '#define ICON_{abbr}_{icon} "{code}"\t// U+{unicode}\n'
        icon_name = str.upper( icon[ 0 ]).replace( '-', '_' )
        icon_code = repr( chr( int( icon[ 1 ], 16 )).encode( 'utf-8' ))[ 2:-1 ]
        result = tmpl_line_icon.format( abbr = cls.intermediate.get( 'font_abbr' ),
                                        icon = icon_name,
                                        code = icon_code,
                                        unicode =icon[ 1 ] )
        return result

    @classmethod
    def convert_ttf_to_header( cls ):
        for ttf in cls.intermediate.get( 'ttfs' ):
            # retrieve and read ttf file
            if 'http' in ttf[ 2 ]:
                # download and read (if file is on GitHub, add '?raw=true')
                response = requests.get( ttf[ 2 ] + '?raw=true' if 'github.com' in ttf[ 2 ] else ttf[ 2 ], timeout = 2 )
                if response.status_code == 200:
                    ttf_data = response.content
                    print( 'ttf file downloaded - ' + ttf[ 1 ] )
                else:
                    raise Exception( 'ttf file missing - ' + ttf[ 2 ])
            else:
                # open from disk and read
                if os.path.isfile( ttf[ 2 ] ):
                    with open( ttf[ 2 ], 'rb' ) as f:
                        ttf_data = f.read()
                        f.close()
                        print( 'ttf file read - ' + ttf[ 1 ])
                else:
                    raise Exception( 'ttf file missing - ' + ttf[ 2 ])
            # convert to header and save to disk
            if ttf_data:
                # convert ttf to header
                tmpl_prelude_ttf = '// Generated by https://github.com/juliettef/IconFontCppHeaders script GenerateIconFontCppHeaders.py for languages {lang}\n' + \
                                   '// from {ttf_file}\n' + \
                                   '// Requires #include <stdint.h>\n' + \
                                   '#pragma once\n\n' + \
                                   'static const uint8_t s_{name}_ttf[{size}] = \n{{'
                result = tmpl_prelude_ttf.format( lang = cls.language_name,
                                                  ttf_file = ttf[ 2 ],
                                                  name = str( ttf[ 1 ][ :-len('.ttf') ].replace( '-', '_' ).replace( ' ', '' )),
                                                  size = str( len( ttf_data )))
                n = 0
                for byte in ttf_data:
                    if (n % 16) == 0:
                        result += '\n\t'
                    result += "0x" + str( hex( int( byte / 16 ))[ 2: ]) + str( hex( byte % 16 )[ 2: ]) + ", "
                    n += 1
                result += '\n};\n\n'
                # save to disk
                ttf_header_file_name = cls.file_name.format( name = str( cls.intermediate.get( 'font_name' )).replace( ' ', '' )) + '_' + ttf[ 1 ] + '.h'
                with open( ttf_header_file_name, 'w' ) as f:
                    f.write( result )
                    f.close()
                print( 'ttf File Saved - {!s}'.format( ttf_header_file_name ))
            else:
                raise Exception( 'Failed ttf to header conversion' + ttf[ 1 ] )


class LanguageCSharp( Language ):
    language_name = "C#"
    file_name = 'Icons{name}.cs'

    @classmethod
    def prelude( cls ):
        tmpl_prelude = '// Generated by https://github.com/juliettef/IconFontCppHeaders script GenerateIconFontCppHeaders.py for language {lang}\n' + \
            '// from {font_data}\n' + \
            '// for use with {ttf_files}\n' + \
            'namespace IconFonts\n' + \
            '{{\n' + \
            '    public class {font_name}\n' + \
            '    {{\n'
        ttf_files = []
        for ttf in cls.intermediate.get( 'ttfs' ):
            ttf_files.append(ttf[ 2])
        result = tmpl_prelude.format(lang = cls.language_name,
                                     font_data = cls.intermediate.get( 'font_data' ),
                                     ttf_files = ', '.join( ttf_files ),
                                     font_name = cls.intermediate.get( 'font_name' ).replace( ' ', '' )
                                     )
        tmpl_prelude_define_file_name = '        public const string FontIconFileName = "{file_name_ttf}";\n'
        for ttf in cls.intermediate.get( 'ttfs' ):
            result += tmpl_prelude_define_file_name.format( file_name_ttf = ttf[ 1 ])
        return result + '\n'

    @classmethod
    def epilogue( cls ):
        return '    }\n' + \
            '}\n'

    @classmethod
    def lines_minmax( cls ):
        tmpl_line_minmax = '        public const int Icon{minmax} = 0x{val};\n'
        result = tmpl_line_minmax.format(minmax = 'Min',
                                         val = cls.intermediate.get( 'font_min' )) + \
                 tmpl_line_minmax.format(minmax = 'Max',
                                         val = cls.intermediate.get( 'font_max' ))
        return result

    @classmethod
    def line_icon( cls, icon ):

        tmpl_line_icon = '        public const string {icon} = "\\u{code}";\n'
        icon_name = cls.to_camelcase(icon[ 0 ])
        icon_code = icon[ 1 ]

        if icon_name[ 0 ].isdigit():
            # Variable may not start with a digit
            icon_name = 'The' + icon_name

        if icon_name == cls.intermediate.get( 'font_name' ).replace( ' ', '' ):
            # Member may not have same name as enclosing class
            icon_name += 'Icon'

        result = tmpl_line_icon.format( icon = icon_name,
                                        code = icon_code)
        return result

    @classmethod
    def to_camelcase( cls, text ):
        parts = text.split( '-' )
        for i in range( len( parts ) ):
            p = parts[i]
            parts[ i ] = p[ 0 ].upper() + p[ 1: ].lower()
        return ''.join( parts )


class LanguageGolang( Language ):
    language_name = "Go"
    file_name = 'icons{name}.go'

    @classmethod
    def prelude( cls ):
        tmpl_prelude = '// Generated by https://github.com/juliettef/IconFontCppHeaders script GenerateIconFontCppHeaders.py for language {lang}\n' + \
            '// from {font_data}\n' + \
            '// for use with {ttf_files}\n' + \
            'package iconfonts\n' + \
            '\n' + \
            'const (\n'
        ttf_files = []
        for ttf in cls.intermediate.get( 'ttfs' ):
            ttf_files.append(ttf[ 2])
        result = tmpl_prelude.format(lang = cls.language_name,
                                     font_data = cls.intermediate.get( 'font_data' ),
                                     ttf_files = ', '.join( ttf_files ),
                                     font_name = cls.intermediate.get( 'font_name' ).replace( ' ', '' )
                                     )
        tmpl_prelude_define_file_name = '\tFontIconFileName{font_abbr} = "{file_name_ttf}"\n'
        for ttf in cls.intermediate.get( 'ttfs' ):
            result += tmpl_prelude_define_file_name.format( font_abbr = ttf[ 0 ], file_name_ttf = ttf[ 1 ])
        return result + '\n'

    @classmethod
    def epilogue( cls ):
        return ')\n'

    @classmethod
    def lines_minmax( cls ):
        tmpl_line_minmax = '\tIcon{minmax} int = 0x{val}\n'
        result = tmpl_line_minmax.format(minmax = 'Min',
                                         val = cls.intermediate.get( 'font_min' )) + \
                 tmpl_line_minmax.format(minmax = 'Max',
                                         val = cls.intermediate.get( 'font_max' )) + '\n'
        return result

    @classmethod
    def line_icon( cls, icon ):
        tmpl_line_icon = '\tIcon{abbr}{icon} string = "\\u{code}"\t// U+{unicode}\n'
        icon_name = cls.to_camelcase(icon[ 0 ])
        icon_code = icon[ 1 ]

        if icon_name[ 0 ].isdigit():
            # Variable may not start with a digit
            icon_name = 'The' + icon_name

        if icon_name == cls.intermediate.get( 'font_name' ).replace( ' ', '' ):
            # Member may not have same name as enclosing class
            icon_name += 'Icon'

        result = tmpl_line_icon.format( icon = icon_name.ljust(32),
                                        code = icon_code,
                                        abbr = cls.intermediate.get( 'font_abbr' ).lower().capitalize(),
                                        unicode = icon[1])
        return result

    @classmethod
    def to_camelcase( cls, text ):
        parts = text.split( '-' )
        for i in range( len( parts ) ):
            p = parts[i]
            parts[ i ] = p[ 0 ].upper() + p[ 1: ].lower()
        return ''.join( parts )

# Main
fonts = [ FontFA4, FontFA5, FontFA5Brands, FontFA5Pro, FontFA5ProBrands, FontFK, FontKI, FontFAD ] # FontMD - Issue #19
languages = [ LanguageC, LanguageCSharp, LanguageGolang ]
ttf2headerC = False # convert ttf files to C and C++ headers

intermediates = []
for font in fonts:
    try:
        font_intermediate = font.get_intermediate_representation()
        if font_intermediate:
            intermediates.append( font_intermediate )
    except Exception as e:
        print( '[ ERROR: {!s} ]'.format( e ))
if intermediates:
    for interm in intermediates:
        Language.intermediate = interm
        for lang in languages:
            if lang:
                lang.save_to_file()
                if ttf2headerC and lang == LanguageC:
                    try:
                        lang.convert_ttf_to_header()
                    except Exception as e:
                        print( '[ ERROR: {!s} ]'.format( e ))
