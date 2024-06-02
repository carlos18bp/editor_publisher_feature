Aquí tienes un ejemplo de un README.md en inglés para tu proyecto actual:

---

# Blog Management Application

## Overview

This project is a blog management application that allows users to create, edit, and delete blog posts using a rich text editor (WYSIWYG). The application implements full CRUD functionality (Create, Read, Update, Delete) for blog posts. The rich text editor enables users to format their content as desired, including the ability to embed images, links, and other media.

## Blog Model

The `Blog` model represents a blog post with the following attributes:
- **title**: The title of the blog post.
- **content**: The content of the blog post, stored as HTML.
- **image_header**: An optional header image for the blog post.
- **created_at**: The date and time when the blog post was created.
- **updated_at**: The date and time when the blog post was last updated.

## Views

### Blog List View
- **URL**: `/blogs/`
- **Methods**: GET, POST
- **Description**: This view lists all blog posts and allows the creation of new blog posts. The blog posts are displayed in descending order of their creation date.

### Blog Update View
- **URL**: `/blogs/update/<int:id>/`
- **Methods**: PUT
- **Description**: This view allows updating an existing blog post identified by its ID.

### Blog Delete View
- **URL**: `/blogs/delete/<int:id>/`
- **Methods**: DELETE
- **Description**: This view allows deleting an existing blog post identified by its ID.

## Running the Project

To run this project, you need to have two servers running: one for the Django backend and another for the Vue.js frontend.

### Backend (Django)

1. **Clone the repository**:
    ```bash
    git clone https://github.com/carlos18bp/editor_publisher_feature
    cd editor_publisher_feature
    ```

2. **Install virtualenv**:
    ```bash
    pip install virtualenv
    ```

3. **To create a new virtual env**:
    ```bash
    virtualenv name_virtual_env
    ```

4. **Create virtual env**:
    ```bash
    virtualenv editor_publisher_feature_env
    ```

5. **Activate virtual env**:
    ```bash
    source editor_publisher_feature_env/bin/activate
    ```

6. **Create dependencies file**:
    ```bash
    pip freeze > requirements.txt
    ```

7. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

8. **Desactivate virtual env**:
    ```bash
    deactivate
    ```

9. **Set up the database**:
    ```bash
    python manage.py migrate
    ```

10. **Create a superuser** (follow the prompts to create an admin user):
    ```bash
    python manage.py createsuperuser
    ```

11. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

### Frontend (Vue.js)

1. **Navigate to the frontend directory**:
    ```bash
    cd frontend
    ```

2. **Install the dependencies**:
    ```bash
    npm install
    ```

3. **Run the development server**:
    ```bash
    npm run serve
    ```

### Accessing the Application

- **Backend**: The Django development server will be running at `http://127.0.0.1:8000/`.
- **Frontend**: The Vue.js development server will be running at `http://localhost:5173/`.

### Notes

- Ensure that both servers are running simultaneously for the application to function correctly.
- For production deployment, you will need to configure a production server and ensure both the backend and frontend are properly set up and secured.

