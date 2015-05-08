'use strict';

var gulp = require('gulp');
var gutil = require('gulp-util');
var checkstyleFileReporter = require('jshint-checkstyle-file-reporter');

var $ = require('gulp-load-plugins')();
var del = require('del');
var runSequence = require('run-sequence');
var bower = require('gulp-bower');

process.env.JSHINT_CHECKSTYLE_FILE = 'jshint.xml';

var buildPaths = {
    publicRoot: 'dist/public',
    adminRoot: 'dist/admin'
};

buildPaths.patterns = {
    js: /\.js$/,
    css: /\.css$/
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
    ]
};

gulp.task('jshint', function () {
    var jsPaths = [];
    jsPaths.push.apply(jsPaths, devWatchPaths.jsPublic);
    jsPaths.push.apply(jsPaths, devWatchPaths.jsAdmin);

   return gulp.src(jsPaths)
       .pipe($.jshint())
       .pipe($.jshint.reporter('jshint-stylish'))
       .pipe($.jshint.reporter(checkstyleFileReporter));
});

gulp.task('bower', function() {
    return bower()
});

gulp.task('stylevendor_public', function () {
    /* {filter: buildPaths.patterns.css} */
    return gulp.src('bower_components/bootstrap-theme-bootswatch-flatly/css/bootstrap.min.css')
        .pipe($.concat('lib.css'))
        .pipe(gulp.dest('dist/public/css'))
        .pipe($.size({title: 'CSS - public vendor'}))
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

gulp.task('default', ['clean'], function (cb) {
   runSequence('bower', ['styles', 'jshint'], cb);
});

gulp.task('build:prod', ['clean'], function (cb) {
    runSequence('bower', ['stylevendor_public', 'styles', 'jshint'], cb)
});
