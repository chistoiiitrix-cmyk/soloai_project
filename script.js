const toolsGrid = document.getElementById('tools-grid');
const searchInput = document.getElementById('searchInput');

async function loadTools() {
    try {
        const response = await fetch('tools.json');
        const tools = await response.json();
        renderTools(tools);
        
        searchInput.addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase();
            const filtered = tools.filter(tool => 
                tool.name.toLowerCase().includes(term) || 
                tool.description.toLowerCase().includes(term) ||
                tool.category.toLowerCase().includes(term)
            );
            renderTools(filtered);
        });
    } catch (error) {
        console.error('Error loading tools:', error);
        toolsGrid.innerHTML = '<p>Error loading tools. Please try again later.</p>';
    }
}

function renderTools(tools) {
    toolsGrid.innerHTML = '';
    if (tools.length === 0) {
        toolsGrid.innerHTML = '<p style="grid-column: 1/-1; text-align: center;">No tools found matching your search.</p>';
        return;
    }
    
    tools.forEach(tool => {
        const card = document.createElement('div');
        card.className = 'tool-card';
        card.innerHTML = `
            <span class="category">${tool.category}</span>
            <h3>${tool.name}</h3>
            <p>${tool.description}</p>
            <a href="${tool.url}" target="_blank" class="btn-visit">Try for Free →</a>
        `;
        toolsGrid.appendChild(card);
    });
}

loadTools();
