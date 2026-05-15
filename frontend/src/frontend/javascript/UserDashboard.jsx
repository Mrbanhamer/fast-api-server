function UserDashboard() {
    const [user, setUser] = React.useState(null);
    const [tasks, setTasks] = React.useState([]);
    const [taskTitle, setTaskTitle] = React.useState("");

    // --- Fetch Data ---
    const loadAllData = async () => {
        try {
            // Get User Profile
            const userRes = await fetch('/user/me', { credentials: 'include' });
            if (!userRes.ok) throw new Error("Unauthorized");
            const userData = await userRes.json();
            setUser(userData);

            // Get User Tasks
            const taskRes = await fetch('/tasks/', { credentials: 'include' });
            const taskData = await taskRes.json();
            setTasks(Array.isArray(taskData) ? taskData : []);
        } catch (err) {
            console.error("Session expired or invalid:", err);
            window.location.href = "/user/login";
        }
    };

    React.useEffect(() => {
        loadAllData();
    }, []);

    // --- Actions ---
    const handleAddTask = async (e) => {
        e.preventDefault();
        if (!taskTitle.trim()) return;

        const response = await fetch('/tasks/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                title: taskTitle, 
                description: "New task from dashboard", 
                completed: false 
            }),
            credentials: 'include'
        });

        if (response.ok) {
            setTaskTitle("");
            loadAllData(); // Refresh list
        }
    };

    const handleDeleteTask = async (taskId) => {
        const response = await fetch(`/tasks/${taskId}`, {
            method: 'DELETE',
            credentials: 'include'
        });

        if (response.ok) {
            setTasks(prev => prev.filter(t => t.id !== taskId));
        }
    };

    const handleToggleComplete = async (task) => {
        await fetch(`/tasks/${task.id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                title: task.title, 
                description: task.description, 
                completed: !task.completed 
            }),
            credentials: 'include'
        });
        loadAllData(); 
    };

    if (!user) return <div style={{ padding: '20px' }}>Loading...</div>;

    return (
        <div style={{ maxWidth: '600px', margin: '40px auto', fontFamily: 'Arial, sans-serif', padding: '0 20px' }}>
            {/* Header Section with Logout */}
            <header style={{ 
                borderBottom: '2px solid #eee', 
                paddingBottom: '15px', 
                marginBottom: '30px',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
            }}>
                <div>
                    <h2 style={{ margin: 0 }}>Welcome, {user.name} {user.last_name}</h2>
                    <p style={{ color: '#666', margin: '5px 0 0 0' }}>{user.email}</p>
                </div>
                
                <a 
                    href="/user/logout" 
                    style={{ 
                        padding: '10px 18px', 
                        backgroundColor: '#6c757d', 
                        color: 'white', 
                        textDecoration: 'none', 
                        borderRadius: '6px',
                        fontSize: '14px',
                        fontWeight: 'bold',
                        transition: 'background 0.2s'
                    }}
                    onMouseOver={(e) => e.target.style.backgroundColor = '#5a6268'}
                    onMouseOut={(e) => e.target.style.backgroundColor = '#6c757d'}
                >
                    Logout
                </a>
            </header>

            {/* Add Task Form */}
            <section>
                <form onSubmit={handleAddTask} style={{ display: 'flex', gap: '10px', marginBottom: '30px' }}>
                    <input 
                        type="text"
                        placeholder="What needs to be done?"
                        value={taskTitle}
                        onChange={(e) => setTaskTitle(e.target.value)}
                        style={{ flex: 1, padding: '12px', borderRadius: '6px', border: '1px solid #ccc', fontSize: '16px' }}
                    />
                    <button type="submit" style={{ padding: '10px 20px', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: 'bold' }}>
                        Add Task
                    </button>
                </form>
            </section>

            {/* Task List Container */}
            <section style={{ background: '#f8f9fa', borderRadius: '12px', padding: '20px', border: '1px solid #e9ecef' }}>
                <h3 style={{ marginTop: 0, marginBottom: '20px' }}>Your Tasks</h3>
                {tasks.length === 0 ? (
                    <p style={{ color: '#888', textAlign: 'center', padding: '20px' }}>No tasks yet. Add one above!</p>
                ) : (
                    <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                        {tasks.map(task => (
                            <li key={task.id} style={{ 
                                background: 'white', 
                                marginBottom: '12px', 
                                padding: '15px', 
                                borderRadius: '8px', 
                                display: 'flex', 
                                justifyContent: 'space-between',
                                alignItems: 'center',
                                boxShadow: '0 2px 4px rgba(0,0,0,0.05)',
                                border: '1px solid #eee'
                            }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                                    <input 
                                        type="checkbox" 
                                        checked={task.completed} 
                                        onChange={() => handleToggleComplete(task)} 
                                        style={{ width: '18px', height: '18px', cursor: 'pointer' }}
                                    />
                                    <span style={{ 
                                        fontSize: '16px',
                                        color: task.completed ? '#adb5bd' : '#212529',
                                        textDecoration: task.completed ? 'line-through' : 'none' 
                                    }}>
                                        {task.title}
                                    </span>
                                </div>
                                <button 
                                    onClick={() => handleDeleteTask(task.id)}
                                    style={{ 
                                        backgroundColor: 'transparent', 
                                        color: '#dc3545', 
                                        border: '1px solid #dc3545', 
                                        padding: '6px 12px', 
                                        borderRadius: '4px', 
                                        cursor: 'pointer',
                                        fontSize: '13px'
                                    }}
                                    onMouseOver={(e) => { e.target.style.backgroundColor = '#dc3545'; e.target.style.color = 'white'; }}
                                    onMouseOut={(e) => { e.target.style.backgroundColor = 'transparent'; e.target.style.color = '#dc3545'; }}
                                >
                                    Delete
                                </button>
                            </li>
                        ))}
                    </ul>
                )}
            </section>
        </div>
    );
}