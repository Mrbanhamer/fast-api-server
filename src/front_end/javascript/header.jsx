function Header() {
    // Only these two for now to keep it clean
    const menuItems = ["login", "signup"];

    const handleMenuClick = (item) => {
        // This moves the user to the HTML page so they can see the form
        window.location.href = `/user/signup`; 
    };

    return (
        <header className="header" style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center', 
            padding: '10px 20px',
            backgroundColor: '#f4f4f4',
            borderBottom: '1px solid #ddd'
        }}>
            <h1 style={{ margin: 0 }}>Mini Project</h1>
            <nav>
                {menuItems.map((item) => (
                    <button 
                        key={item} 
                        onClick={() => handleMenuClick(item)}
                        style={{ 
                            marginLeft: '10px',
                            padding: '8px 15px',
                            cursor: 'pointer',
                            textTransform: 'capitalize',
                            borderRadius: '5px',
                            border: '1px solid #ccc',
                            backgroundColor: 'white'
                        }}
                    >
                        {item}
                    </button>
                ))}
            </nav>
        </header>
    );
}