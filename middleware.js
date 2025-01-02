
module.exports.isLoggedIn = (req, res, next) => {

    if (!req.isAuthenticated()) {   // checks current session me user logged in h ki nhi as passport user info save karata h
        req.session.redirectUrl = req.originalUrl; //but passport jaese hi login krte hai redirectUrl ko reset krdeta hai isiliye save bhi karana padega agl se
        //res.locals variables me kyuki passport ke pass access ni h delete krna ka usko
        console.log("req.originalUrl", req.originalUrl);

        req.flash("error", "you must be logged in");
        return res.redirect("/login")
    }
    next();
}
module.exports.saveRedirectUrl = (req, res, next) => {
    if (req.session.redirectUrl) {
        res.locals.redirectUrl = req.session.redirectUrl;
    }
    next();
}

