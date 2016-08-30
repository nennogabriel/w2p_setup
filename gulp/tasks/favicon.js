var gulp   = require('gulp'),
    config = require('../config'),
    imageResize = require('gulp-image-resize'),
    imagemin = require('gulp-imagemin'),
    squareSize = function(size){ return { width: size, height: size, crop: true, upscale: false }},
    rename = require('gulp-rename');



gulp.task("favicon", function () {
    gulp.src(config.folder.local + "static/icon.png")
        .pipe(imageResize( squareSize(32)))
        .pipe(imagemin({ progressive: true, interlaced: true}))
        .pipe(rename(function (path){
            path.basename = "favicon";
            path.extname = ".ico";
            path.dirname = "./static/";
            console.log(path);
        }))
        .pipe(gulp.dest(config.folder.base));
    gulp.src(config.folder.local + "static/icon.png")
        .pipe(imageResize( squareSize(192)))
        .pipe(imagemin({ progressive: true, interlaced: true}))
        .pipe(rename(function (path){
            path.basename = "chrome-touch-icon-192x192";
            path.dirname = "./static/";
        }))
        .pipe(gulp.dest(config.folder.base));
    gulp.src(config.folder.local + "static/icon.png")
        .pipe(imageResize( squareSize(192)))
        .pipe(imagemin({ progressive: true, interlaced: true}))
        .pipe(rename(function (path){
            path.basename = "apple-touch-icon";
            path.dirname = "./static/";
        }))
        .pipe(gulp.dest(config.folder.base));
    gulp.src(config.folder.local + "static/icon.png")
        .pipe(imageResize( squareSize(144)))
        .pipe(imagemin({ progressive: true, interlaced: true}))
        .pipe(rename(function (path){
            path.basename = "ms-touch-icon-144x144-precomposed";
            path.dirname = "./static/";
        }))
        .pipe(gulp.dest(config.folder.base));
});