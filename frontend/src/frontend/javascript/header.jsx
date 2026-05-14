function Header() {
    // Added 'profile' to the list so you can navigate back to your dashboard
    const menuItems = ["login", "signup", "profile"];

    const handleMenuClick = (item) => {
        // Use backticks (`) and ${item} to make the URL dynamic!
        // This will send you to /user/login, /user/signup, or /user/profile
        if (item === "profile") {
            window.location.href = `/user/`; // Your protected route
        } else {
            window.location.href = `/user/${item}`;
        }
    };

    return (
        <header className="header" style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center', 
            padding: '10px 40px',
            backgroundColor: '#2c3e50',
            color: 'white',
            boxShadow: '0 2px 5px rgba(0,0,0,0.1)'
        }}>
            <h1 
                onClick={() => window.location.href = '/'} 
                style={{ cursor: 'pointer', margin: 0, fontSize: '24px' }}
            >
                My App
            </h1>
            <nav>
                {menuItems.map((item) => (
                    <button 
                        key={item} 
                        onClick={() => handleMenuClick(item)}
                        style={{ 
                            marginLeft: '15px',
                            padding: '8px 20px',
                            cursor: 'pointer',
                            textTransform: 'capitalize',
                            borderRadius: '4px',
                            border: '1px solid #ecf0f1',
                            backgroundColor: 'transparent',
                            color: 'white',
                            transition: '0.3s'
                        }}
                        onMouseOver={(e) => e.target.style.backgroundColor = '#34495e'}
                        onMouseOut={(e) => e.target.style.backgroundColor = 'transparent'}
                    >
                        {item}
                    </button>
                ))}
            </nav>
        </header>
    );
}