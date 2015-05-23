'use strict';

var gulp = require('gulp');
var gutil = require('gulp-util');
var jshintXMLReporter = require('gulp-jshint-xml-file-reporter');

var $ = require('gulp-load-plugins')();
var del = require('del');
var runSequence = require('run-sequence');
var bower = require('gulp-bower');
var mainBowerFiles = require('main-bower-files');

var buildPaths = {
    publicRoot: 'dist/public',
    adminRoot: 'dist/admin'
};

buildPaths.patterns = {
    js: /\.js$/,
    css: /\.css$/,
    jsPublic: ['bower_components/jquery/dist/**/*.min.js', 'bower_components/bootstrap/dist/js/**/*.min.js']
};

buildPaths.hermes = {
    jsAdmin: 'dist/admin/js',
    jsPublic: 'dist/public/js',
    templates: 'dist/admin/templates'
};

var devWatchPaths = {
    jsPublic: [
        'src/public/js/**/*'
    ],
    jsAdmin: [
        'src/admin/js/**/*'
    ],
    cssAdmin: [
        'src/admin/css/**/*'
    ],
    cssPublic: [
        'src/public/css/**/*'
    ],
    templates: 'src/admin/templates/**/*.html'
};

gulp.task('jshint', function () {
    var jsPaths = [];
    jsPaths.push.apply(jsPaths, devWatchPaths.jsPublic);
    jsPaths.push.apply(jsPaths, devWatchPaths.jsAdmin);

   return gulp.src(jsPaths)
       .pipe($.jshint())
       .pipe($.jshint.reporter('jshint-stylish'))
       .pipe($.jshint.reporter(jshintXMLReporter))
       .on('end', jshintXMLReporter.writeFile({
           format: 'checkstyle',
           filePath: './jshint.xml',
           alwaysReport: true
       }));
});

gulp.task('jsvendor_admin', function() {
    return gulp.src(mainBowerFiles({ filter: buildPaths.patterns.js }))
        .pipe($.concat('lib.js', { newLine: ';\n' }))
        .pipe(gulp.dest(buildPaths.hermes.jsAdmin));
});

gulp.task('jsvendor_public', function() {
    return gulp.src(buildPaths.patterns.jsPublic)
        .pipe($.concat('lib.js', { newLine: ';\n' }))
        .pipe(gulp.dest(buildPaths.hermes.jsPublic));
});

gulp.task('jscopy', ['jsvendor_admin', 'jsvendor_public'], function() {
    gulp.src(devWatchPaths.jsAdmin)
        .pipe($.concat('app.js'))
        .on('error', function (err) {
            gutil.log(err.message)
            this.emit('end')
        })
        .pipe($.ngAnnotate())
        .on('error', function (err) {
            gutil.log(err.message)
            this.emit('end')
        })
        .pipe(gulp.dest(buildPaths.hermes.jsAdmin))
        .pipe($.size({title: 'js_uncompressed'}));
})

gulp.task('views', function () {
    return gulp.src(devWatchPaths.templates)
        .pipe($.angularTemplatecache('template.js', {
            standalone: true,
            root: 'templates/',
            module: 'hermes.templates'
        }))
        .pipe(gulp.dest(buildPaths.hermes.templates));
});

gulp.task('bower', function() {
    return bower();
});

gulp.task('stylevendor_public', function () {
    /* {filter: buildPaths.patterns.css} */
    return gulp.src('bower_components/bootstrap-theme-bootswatch-flatly/css/bootstrap.min.css')
        .pipe($.concat('lib.css'))
        .pipe(gulp.dest('dist/public/css'))
        .pipe($.size({title: 'CSS - public vendor'}));
});

gulp.task('styles_admin', function () {
   return gulp.src(devWatchPaths.cssAdmin)
       .pipe($.sass({
           precision: 3,
           style: 'nested',
           onError: function (error) {
               console.error(error)
           }
       }))
       .pipe($.concat('app.css'))
       .pipe(gulp.dest('dist/admin/css'))
       .pipe($.size({title: 'Admin CSS'}));
});

gulp.task('styles_public', function () {
    return gulp.src(devWatchPaths.cssPublic)
        .pipe($.sass({
            precision: 3,
            style: 'nested',
            onError: function (error) {
                console.error(error)
            }
        }))
        .pipe($.concat('app.css'))
        .pipe(gulp.dest('dist/public/css'))
        .pipe($.size({title: 'Public CSS'}));
});

gulp.task('clean', del.bind(null, [
    'dist/*',
    '!dist/.git'
], {
    dot: true
}));

gulp.task('styles', function () {
    runSequence('bower', ['styles_public', 'styles_admin', 'stylevendor_public']);
});

gulp.task('watch', function () {
    gulp.watch('src/admin/templates/**/*.html', ['views']);
    gulp.watch('src/**/*.{css,scss}', ['styles']);
    gulp.watch('src/admin/js/**/*.js', ['jshint', 'jscopy']);
});

gulp.task('default', ['clean'], function (cb) {
   runSequence('bower', ['styles', 'jshint', 'views', 'jscopy', 'watch'], cb);
});

gulp.task('build:prod', ['clean'], function (cb) {
    runSequence('bower', ['styles', 'jshint', 'views', 'jscopy'], cb);
});
