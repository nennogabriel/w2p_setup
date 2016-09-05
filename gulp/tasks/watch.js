
var gulp   = require('gulp'),
    config = require('../config'),
    livereload = require('gulp-livereload');


gulp.task("watch", function (){
    livereload.listen();
    gulp.watch(config.folder.app + "{controllers,models,modules,views,static}/**/*", function (e){gulp.src(e.path).pipe(livereload())});
    gulp.watch(["./charmcss/**/*.{sass,scss}", config.folder.local + "**/*.{sass,scss}"], ["sass"]);
    gulp.watch(config.folder.local + "**/*.js", ["uglify"]);
});