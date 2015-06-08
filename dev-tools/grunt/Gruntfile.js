module.exports = function(grunt) {
    grunt.initConfig({
        watch: {
            options: {
                livereload: true
            },
            livereload: {
                files: [
                    '../../survival/**/*.html', 
                    '../../survival/**/*.css', 
                    '../../survival/**/*.js'
                ]
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-watch'); 

    grunt.registerTask('default', [
        // add all tasks you need including watch
        'watch' 
    ]);
};