// Load existing posts with comments from local storage or initialize an empty array
let postsData = JSON.parse(localStorage.getItem('savedPosts')) || [];

// Function to display posts and comments
function displayPosts() {
    const postsSection = document.getElementById('posts');
    postsSection.innerHTML = '';

    postsData.forEach((post, index) => {
        const postElement = document.createElement('div');
        postElement.className = 'post';

        postElement.innerHTML = `
            <span style="font-size: 25px; font-style: bold; font-weight:bold">${post.username}</span>
            <br> 
            <span style="margin-bottom: 32px;"> ${post.content}</form><br>
            <button style="background-color: #333;height:40px; width:100px;color: azure;border-radius: 5px; margin-top: 10px" id="show-comments" onclick="toggleComments(${index})">Show Comments</button>
            <div id="comments-${index}" style="display:none;">
                ${renderComments(post.comments)}
            </div>
            <form id="commentForm-${index}" class="comment-form" style="display:none;">
                <input type="text" id="commentUsername-${index}" placeholder="Your username">
                <textarea id="commentContent-${index}" placeholder="Write your comment here..."></textarea>
                <button type="submit">Comment</button>
            </form>
        `;
        postsSection.appendChild(postElement);

        const commentForm = document.getElementById(`commentForm-${index}`);
        commentForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const commentUsername = document.getElementById(`commentUsername-${index}`).value;
            const commentContent = document.getElementById(`commentContent-${index}`).value;
            if (commentUsername.trim() !== '' && commentContent.trim() !== '') {
                postsData[index].comments.push({ username: commentUsername, content: commentContent });
                savePostsData(); // Save updated postsData to local storage
                displayPosts();
                document.getElementById(`commentUsername-${index}`).value = '';
                document.getElementById(`commentContent-${index}`).value = '';
            }
        });
    });
}

// Function to render comments
function renderComments(comments) {
    if (comments.length === 0) return '<p>No comments yet.</p>';
    return comments.map(comment => `<div class="comment"><span style="font-size: 25px; color: #067e52; font-weight:bold">${comment.username}</span> <br> ${comment.content}</div>`).join('');
}

// Function to toggle comments visibility
function toggleComments(index) {
    const commentsDiv = document.getElementById(`comments-${index}`);
    const commentForm = document.getElementById(`commentForm-${index}`);
    if (commentsDiv.style.display === 'none') {
        commentsDiv.style.display = 'block';
        commentForm.style.display = 'block';
    } else {
        commentsDiv.style.display = 'none';
        commentForm.style.display = 'none';
    }
}

// Function to handle posting a new post
document.getElementById('postForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const postContent = document.getElementById('postContent').value;
    if (username.trim() !== '' && postContent.trim() !== '') {
        postsData.push({ username: username, content: postContent, comments: [] });
        savePostsData(); // Save updated postsData to local storage
        displayPosts();
        document.getElementById('username').value = '';
        document.getElementById('postContent').value = '';
    }
});

// Function to save postsData to local storage
function savePostsData() {
    localStorage.setItem('savedPosts', JSON.stringify(postsData));
}

// Display posts and comments when the page loads
displayPosts();