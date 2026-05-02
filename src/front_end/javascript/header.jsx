import { useNavigate } from 'react-router-dom'; // If using React Router

function Header() {
    const menuItems = ["profile", "store", "settings", "logout"];

    const handleMenuClick = async (item) => {
        if (item === "logout") {
            try {
                // Call the actual logout endpoint we discussed
                const response = await fetch('http://127.0.0.1:8000/user/logout', {
                    method: 'POST',
                    credentials: 'include' // Tells browser to send the cookie to be deleted
                });

                if (response.ok) {
                    window.location.href = 'index.html'; // Go back to start
                }
            } catch (error) {
                console.error('Logout failed:', error);
            }
            return;
        }

        // For other items, just navigate to the page
        // Since you have separate HTML files:
        window.location.href = `${item}.html`;
    };

    return (
        <header className="header">
            <div className="header-inner-container">
                <h1 className="headerlogo" onClick={() => window.location.href = 'user.html'} style={{cursor:'pointer'}}>
                    mini project
                </h1>
                
                <div className="menu-container" style={{ display: 'flex', gap: '20px' }}>
                    {menuItems.map((item) => (
                        <h1 
                            key={item} 
                            className="headerHighlight"
                            onClick={() => handleMenuClick(item)}
                            style={{ cursor: 'pointer', fontSize: '1.2rem' }}
                        >
                            {item}
                        </h1>
                    ))}
                </div>
            </div>
        </header>
    );
}

export default Header;