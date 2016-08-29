
var gulp   = require('gulp'),
    config = require('../config'),
    plumber = require('gulp-plumber'),
    include = require('gulp-include'),
    uglify = require('gulp-uglify'),
    rename = require('gulp-rename');


// Concatenate, compile and ulgify JS
gulp.task("uglify", function(){
    gulp.src(config.folder.local + "*/{js,script,layout}/[^_]*.js")
        // .pipe(plumber())
        .pipe(include())
        .on("error", console.log)
        .pipe(uglify({mangle:true}))
        .pipe(rename(function (path){
            path.extname = ".js";
            path.dirname = path.dirname.replace("00_local/", "");
        }))
        .pipe(gulp.dest(config.folder.base))
});