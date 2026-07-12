const toolsGrid = document.getElementById('tools-grid');
const blogGrid = document.getElementById('blog-grid');
const searchInput = document.getElementById('searchInput');

async function loadData() {
    try {
        // Загружаем оба файла одновременно
        const [toolsRes, articlesRes] = await Promise.all([
            fetch('tools.json'),
            fetch('articles.json').catch(() => null) // Если файла еще нет, не падаем
        ]);
        
        const tools = await toolsRes.json();
        const articles = articlesRes ? await articlesRes.json() : [];
        
        renderTools(tools);
        renderBlog(articles);
        
        // Поиск только по инструментам
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
        console.error('Ошибка при загрузке данных:', error);
    }
}

function renderTools(tools) {
    toolsGrid.innerHTML = '';
    if (tools.length === 0) {
        toolsGrid.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: var(--gray);">Инструменты скоро появятся...</p>';
        return;
    }
    tools.forEach(tool => {
        const card = document.createElement('div');
        card.className = 'tool-card';
        card.innerHTML = `
            <span class="category">${tool.category}</span>
            <h3>${tool.name}</h3>
            <p>${tool.description}</p>
            <a href="${tool.url}" target="_blank" class="btn-visit">Попробовать →</a>
        `;
        toolsGrid.appendChild(card);
    });
}

function renderBlog(articles) {
    blogGrid.innerHTML = '';
    if (articles.length === 0) {
        blogGrid.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: var(--gray);">Статьи скоро появятся...</p>';
        return;
    }
    articles.forEach(article => {
        const card = document.createElement('div');
        card.className = 'blog-card';
        card.innerHTML = `
            <h3>${article.title}</h3>
            <p>${article.summary}</p>
            <a href="#" style="color: var(--primary); font-weight: 600; text-decoration: none; font-size: 0.9rem;">Читать далее →</a>
        `;
        blogGrid.appendChild(card);
    });
}

loadData();
