function NavBar() {
    let userLinks;
    if (_user) {
        userLinks = (
            <>
                <li key="u1"><a href={_userLinks.profileUrl}>Profile</a></li>
                <li key="u2"><a href={_userLinks.logoutUrl+'?next='+_homeLink}>Log Out</a></li>
            </>
        )
    } else {
        userLinks = (
            <>
                <li key="u1"><a href={_userLinks.loginUrl}>Log In</a></li>
                <li key="u2"><a href={_userLinks.registerUrl}>Register</a></li>
            </>
        )
    }

    let accessLinks = [];
    if (_user) {
        if (_user.position_type == 1) { // driver
            
        } if (_user.position_type == 2) { // mechanic
            
        } if (_user.position_type >= 3) { // admin and su
            accessLinks.push(<li key="a1"><a href={_createCheckupFormLink}>Checkup Forms</a></li>)
            accessLinks.push(<li key="a2"><a href="#">Vehicles</a></li>)
            accessLinks.push(<li key="a3"><a href="#">Repairs</a></li>)
        } if (_user.position_type >= 4) { // su
            accessLinks.push(<li key="s1"><a href={_adminLink}>Admin</a></li>)
        }
        accessLinks.push(<li key="sep">-</li>)
    }

    return (
        <nav className="container">
            <ul>
                <li><a href={_homeLink}><strong>MovereFleet</strong></a></li>
            </ul>
            <ul>
                {accessLinks}
                {userLinks}
            </ul>
        </nav>
    );
}