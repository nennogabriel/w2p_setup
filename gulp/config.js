var appsfolder = "./web2py/applications/",
    appname = "init";


module.exports = {
    folder: {
        app: appsfolder + appname + "/",
        local: appsfolder + appname + "/00_local/",
        base: (appname === "*" ? appsfolder : appsfolder + appname + "/")
    }
};
