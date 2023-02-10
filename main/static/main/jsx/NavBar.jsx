function NavBar() {
    let userLinks;
    if (_user) {
        userLinks = (
            <>
                <li><a href={_userLinks.profileUrl}>Profile</a></li>
                <li><a href={_userLinks.logoutUrl+'?next='+_homeLink}>Log Out</a></li>
            </>
        )
    } else {
        userLinks = (
            <>
                <li><a href={_userLinks.loginUrl}>Log In</a></li>
                <li><a href={_userLinks.registerUrl}>Register</a></li>
            </>
        )
    }
    return (
        <nav className="container">
            <ul>
                <li><strong>MovereFleet</strong></li>
            </ul>
            <ul>
                {userLinks}
            </ul>
        </nav>
    );
}