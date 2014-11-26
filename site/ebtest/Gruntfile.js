module.exports = function(grunt) {
    'use strict';

    var static_folder = 'static/';
    var assets = require('grunt-assets')
        .importAssets(grunt, 'assets.json', static_folder);


    // Project configuration.
    grunt.initConfig({
        // Metadata.
        pkg: grunt.file.readJSON('package.json'),
        banner: '/*! <%= pkg.title || pkg.name %>\n' + '<%= pkg.homepage ? "* " + pkg.homepage + "\\n" : "" %>' + '* Copyright (c) <%= grunt.template.today("yyyy") %> <%= pkg.author.name %>; */',

        static_folder: static_folder,

        clean: {
            js: {
                src : ['<%= static_folder %>dist/js/**/*.js']
            },
            jst: {
                src : ['<%= static_folder %>dist/templates/**/*.js']
            },
            css: {
                src : ['<%= static_folder %>dist/css/**/*.css']
            }
        },

        less: assets.getLessConfig(),

        jshint: {
            options: {
                jshintrc: '<%= static_folder %>js/.jshintrc'
            },
            gruntfile: {
                options: {
                    jshintrc: '.jshintrc'
                },
                src: 'Gruntfile.js'
            },
            project : {
                src: '<%= static_folder %>js/**/*.js'
            }
        },

        jst: {
            options: {
                prettify: true,
                processName: function(filename) {
                    return filename
                        .toLowerCase()
                        .replace('static/templates/', '');
                }
            },
            production: {
                files: {
                    '<%= static_folder %>dist/templates/templates.js' : [
                        '<%= static_folder %>templates/**/*.html'
                    ]
                }
            }
        },

        uglify: assets.getUglifyConfig({
            options: {
                banner: '<%= banner %>'
            }
        }),

        watch: {
            gruntfile: {
                files: 'Gruntfile.js',
                tasks: 'jshint:gruntfile',
                options: {
                    livereload: true
                }
            },
            less: {
                files: '<%= static_folder %>less/**/*.less',
                tasks: 'build-css',
                options: {
                    livereload: true
                }
            },
            jst: {
                files: '<%= static_folder %>templates/**/*.html',
                tasks: [
                    'clean:jst',
                    'jst'
                ],
                options: {
                    livereload: true
                }
            },
            js: {
                files: '<%= static_folder %>js/**/*.js',
                tasks: [
                    'clean:js',
                    'uglify'
                ],
                options: {
                    livereload: true
                }
            },

            assets: {
                files: ['assets.json', '**/*.mo'],
                tasks: ['exec:reload_assets']
            }
        },

        connect: {
            server: {
                options: {
                    hostname: '*',
                    port: 9000
                }
            }
        },

        exec : {
            reload_assets : {
                cmd: 'touch settings.py'
            }
        }
    });


    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-contrib-less');

    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-jst');
    grunt.loadNpmTasks('grunt-contrib-uglify');

    grunt.loadNpmTasks('grunt-contrib-watch');

    grunt.loadNpmTasks('grunt-contrib-connect');

    grunt.loadNpmTasks('grunt-exec');

    grunt.registerTask('default', [
        'jshint',
        'build-css',
        'build-js'
    ]);

    grunt.registerTask('build-css', [
        'clean:css',
        'less'
    ]);

    grunt.registerTask('build-js', [
        'clean:jst',
        'clean:js',
        'jst',
        'uglify'
    ]);

    grunt.registerTask('serve', [
        'jshint:gruntfile',
        'build-css',
        'jst',
        'connect',
        'watch'
    ]);
};
