
var gulp = require('gulp');
var browserSync = require('browser-sync');

gulp.task('server', function () {
    browserSync({
        server: {
            baseDir: ['../../hermes_cms/hermes_cms/templates/admin'],
            routes: {
                '/admin': '../../hermes_cms/hermes_cms/templates/admin',
                '/assets': '../../hermes_ui/dist'
            }
        }
    })
});
