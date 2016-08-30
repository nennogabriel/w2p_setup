var gulp   = require('gulp'),
    config = require('../config'),
    plumber = require('gulp-plumber'),
    sass = require('gulp-sass'),
    autoprefixer = require('gulp-autoprefixer'),
    minifyCss = require('gulp-minify-css'),
    rename = require('gulp-rename'),
    autoprefixeroptions = {browser : ["> 0.30% in BR", "last 2 versions", "ie > 7", "iOS > 6"]};


gulp.task("sass", function(){
    gulp.src( config.folder.local + "*/{css,inline}/[^_]*.{sass,scss}")
        .pipe(plumber())
        .pipe(sass({includePaths : ['./']}))
        .pipe(autoprefixer( autoprefixeroptions ))
        .pipe(minifyCss( {compatibility: "ie8", processImport: false, keepSpecialComments: 0} ))
        .pipe(rename(function(path){
            path.extname = ".css";
            path.dirname = path.dirname.replace("00_local", "")
        }))
        .pipe(gulp.dest(config.folder.base))
});

