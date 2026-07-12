const toolsGrid = document.getElementById('tools-grid');
const blogGrid = document.getElementById('blog-grid');
const searchInput = document.getElementById('searchInput');
const modal = document.getElementById('articleModal');
const modalBody = document.getElementById('modalBody');
const closeModal = document.querySelector('.close-modal');

let allArticles = [];

async function loadData() {
    try {
        const [toolsRes, articlesRes] = await Promise.all([
            fetch('tools.json'),
            fetch('articles.json').catch(() => null)
        ]);
        
        const tools = await toolsRes.json();
        allArticles = articlesRes ? await articlesRes.json() : [];
        
        renderTools(tools);
        renderBlog(allArticles);
        
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
        console.error('Ошибка загрузки данных:', error);
    }
}

function renderTools(tools) {
    toolsGrid.innerHTML = '';
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
    articles.forEach((article, index) => {
        const card = document.createElement('div');
        card.className = 'blog-card';
        card.innerHTML = `
            <h3>${article.title}</h3>
            <p>${article.summary}</p>
            <a href="#" class="read-more" data-index="${index}" style="color: var(--primary); font-weight: 600; text-decoration: none; font-size: 0.9rem;">Читать далее →</a>
        `;
        blogGrid.appendChild(card);
    });

    // Добавляем событие клика на все кнопки "Читать далее"
    document.querySelectorAll('.read-more').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const index = e.target.getAttribute('data-index');
            openArticle(index);
        });
    });
}

function openArticle(index) {
    const article = allArticles[index];
    modalBody.innerHTML = `
        <h1>${article.title}</h1>
        <div class="article-date" style="color: var(--gray); margin-bottom: 1rem;">${article.date}</div>
        <div class="article-text" style="line-height: 1.8; font-size: 1.1rem;">${article.content}</div>
        <br>
        <a href="${article.link}" target="_blank" class="btn-visit" style="display: block; text-align: center; text-decoration: none; background: var(--primary); color: white; padding: 1rem; border-radius: 10px; font-weight: 700;">Перейти к инструменту →</a>
    `;
    modal.style.display = 'block';
}

closeModal.onclick = () => modal.style.display = 'none';
window.onclick = (event) => { if (event.target == modal) modal.style.display = 'none'; };

loadData();
