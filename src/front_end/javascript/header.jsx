function Header() {
    const menuItems = ["profile", "store", "settings", "logout"];

    // 1. Move the function INSIDE the component so it can be used easily
    const handleMenuClick = async (item) => {
        // We use the 'item' (profile, store, etc.) as the action
        const userData = {
            email: "test@example.com", // In a real app, this comes from a state/form
            name: "John",
            last_name: "Doe",
            password: "secretpassword123",
            age: 25,
            action: item // Now it sends 'profile' or 'store' depending on what you click
        };

        try {
            const response = await fetch('/index', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(userData),
            });

            if (response.ok) {
                // If backend verified the action, go to the user route
                window.location.href = '/user/'; 
            } else {
                const errorData = await response.json();
                console.error('Backend Error:', errorData);
            }
        } catch (error) {
            console.error('Network Error:', error);
        }
    };

    return (
        <header className="header">
            <div className="header-inner-container">
                <h1 className="headerlogo">mini project</h1>
                
                {menuItems.map((item) => (
                    <h1 
                        key={item} 
                        className="headerHighlight"
                        onClick={() => handleMenuClick(item)} // 2. Attach the click here
                        style={{ cursor: 'pointer' }}        // 3. Make it look clickable
                    >
                        {item}
                    </h1>
                ))}
            </div>
        </header>
    );
}