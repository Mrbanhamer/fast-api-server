function Header() {
    const menuItems = ["profile", "store", "settings", "logout"];

    return (
        <header className="header">
            <div className="header-inner-container">
                <h1 className="headerlogo">mini project</h1>
                
                {menuItems.map((item) => (
                    <h1 key={item} className="headerHighlight">
                        {item}
                    </h1>
                ))}
            </div>
        </header>
    );
}