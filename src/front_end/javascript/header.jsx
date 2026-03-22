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

const handleProfileClick = async () => {
    const userData = {
        email: "test@example.com",
        name: "John",
        last_name: "Doe",
        password: "secretpassword123", // Must be at least 8 chars per your model
        age: 25
    };

    try {
        const response = await fetch('/index', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userData),
        });

        if (response.ok) {
            window.location.href = '/user';
        } else {
            const errorData = await response.json();
            console.error('Validation Error:', errorData);
        }
    } catch (error) {
        console.error('Network Error:', error);
    }
};