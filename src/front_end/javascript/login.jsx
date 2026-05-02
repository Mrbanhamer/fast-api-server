function Login() {
    const [email, setEmail] = React.useState("");
    const [password, setPassword] = React.useState("");

    const handleLogin = async (e) => {
        e.preventDefault();
        
        // FastAPI OAuth2 expects 'username' and 'password'
        const formData = new FormData();
        formData.append('username', email); 
        formData.append('password', password);

        try {
            const response = await fetch('/user/login', {
                method: 'POST',
                body: formData,
                credentials: 'include' // Important for saving the session cookie
            });

            if (response.ok) {
                alert("Login successful!");
                window.location.href = "/user/profile"; // Redirect to profile
            } else {
                alert("Invalid email or password.");
            }
        } catch (error) {
            console.error("Login error:", error);
            alert("Connection error.");
        }
    };

    return (
        <div style={{ display: 'flex', justifyContent: 'center', marginTop: '50px' }}>
            <form onSubmit={handleLogin} style={{ 
                display: 'flex', 
                flexDirection: 'column', 
                width: '300px', 
                gap: '15px',
                padding: '20px',
                border: '1px solid #ddd',
                borderRadius: '8px'
            }}>
                <h2 style={{ textAlign: 'center' }}>Login</h2>
                
                <input type="email" placeholder="Email" value={email} 
                    onChange={(e) => setEmail(e.target.value)} required />
                
                <input type="password" placeholder="Password" value={password} 
                    onChange={(e) => setPassword(e.target.value)} required />

                <button type="submit" style={{ 
                    padding: '10px', 
                    backgroundColor: '#28a745', 
                    color: 'white', 
                    border: 'none', 
                    borderRadius: '4px',
                    cursor: 'pointer'
                }}>
                    Login
                </button>
            </form>
        </div>
    );
}