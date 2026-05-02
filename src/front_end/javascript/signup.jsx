function Signup() {
    // State to hold form data
    const [name, setName] = React.useState("");
    const [lastName, setLastName] = React.useState("");
    const [email, setEmail] = React.useState("");
    const [password, setPassword] = React.useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Create the FormData object to match your backend's Form(...) requirements
        const formData = new FormData();
        formData.append('name', name);
        formData.append('last_name', lastName);
        formData.append('email', email);
        formData.append('password', password);

        try {
            const response = await fetch('/user/signup', {
                method: 'POST',
                body: formData, // Sending as Form Data, not JSON
                credentials: 'include'
            });

            if (response.ok) {
                alert("Account created successfully!");
                // Your backend returns a redirect, but fetch follows it. 
                // We manually redirect to the dashboard here for clarity.
                window.location.href = "/user/profile"; 
            } else {
                alert("Signup failed. That email might already be taken.");
            }
        } catch (error) {
            console.error("Error:", error);
            alert("Connection error.");
        }
    };

    return (
        <div style={{ display: 'flex', justifyContent: 'center', marginTop: '50px' }}>
            <form onSubmit={handleSubmit} style={{ 
                display: 'flex', 
                flexDirection: 'column', 
                width: '300px', 
                gap: '15px',
                padding: '20px',
                border: '1px solid #ddd',
                borderRadius: '8px'
            }}>
                <h2 style={{ textAlign: 'center' }}>Sign Up</h2>
                
                <input type="text" placeholder="First Name" value={name} 
                    onChange={(e) => setName(e.target.value)} required />
                
                <input type="text" placeholder="Last Name" value={lastName} 
                    onChange={(e) => setLastName(e.target.value)} required />
                
                <input type="email" placeholder="Email Address" value={email} 
                    onChange={(e) => setEmail(e.target.value)} required />
                
                <input type="password" placeholder="Password" value={password} 
                    onChange={(e) => setPassword(e.target.value)} required />

                <button type="submit" style={{ 
                    padding: '10px', 
                    backgroundColor: '#007bff', 
                    color: 'white', 
                    border: 'none', 
                    borderRadius: '4px',
                    cursor: 'pointer'
                }}>
                    Create Account
                </button>
            </form>
        </div>
    );
}