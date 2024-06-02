<template>
  <div>
    <h1 class="font-bold pb-6">Blog Posts</h1>
    <div v-if="store.blogs.length">
      <div v-for="blog in store.blogs" :key="blog.id" class="blog-post">
        <div class="flex justify-between">
          <button
            @click="selectBlog(blog)"
            class="pr-24 text-blue-600 hover:text-blue-800 focus:outline-none">
            {{ blog.title }}
          </button>
          <div class="space-x-6">
            <button
              v-if="!store.isEditing"
              @click="editBlog(blog)"
              type="button" 
              class="text-white bg-gradient-to-r from-cyan-400 via-cyan-500 to-cyan-600 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-cyan-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2">
              Edit Blog
            </button>
            <button
              @click="deleteBlog(blog.id)"
              type="button" 
              class="text-white bg-gradient-to-r from-red-400 via-red-500 to-red-600 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-red-300 shadow-lg shadow-red-500/50 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2">
              Delete
            </button>
          </div>  
        </div>
        <p>Published on: {{ formatDate(blog.created_at) }}</p>
        <p>Last updated on: {{ formatDate(blog.updated_at) }}</p>
      </div>
    </div>
    <div v-else>
      <p>No blog posts available.</p>
    </div>
  </div>
</template>

<script setup>
  import { watchEffect } from 'vue'
  import { useBlogStore } from '@/store/blog'

  // Initialize the blog store
  const store = useBlogStore()

  // Define emitted events
  const emit = defineEmits(['select-blog', 'edit-blog'])

  // Fetch blogs when the component is mounted
  watchEffect(async () => {
    await store.fetchBlogs()
  })

  /**
   * Sets the focused blog and emits the select-blog event.
   * @param {Object} blog - The blog object to focus on.
   */
  const selectBlog = (blog) => {
    store.blogFocus = blog
    emit('select-blog')
  }

  /**
   * Sets the focused blog and emits the edit-blog event.
   * @param {Object} blog - The blog object to edit.
   */
  const editBlog = (blog) => {
    store.blogFocus = blog
    emit('edit-blog')
  }

  /**
   * Deletes a blog by its ID after confirming with the user.
   * @param {number} id - The ID of the blog to delete.
   */
  const deleteBlog = async (id) => {
    if (confirm('Are you sure you want to delete this blog?')) {
      await store.deleteBlog(id)
    }
  }

  /**
   * Formats a date string into a readable format.
   * @param {string} dateString - The date string to format.
   * @returns {string} - The formatted date string.
   */
  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'long', day: 'numeric' }
    return new Date(dateString).toLocaleDateString(undefined, options)
  }
</script>

<style scoped>
  .blog-post {
    margin-bottom: 2rem;
    padding: 1rem;
    border: 1px solid #ddd;
    border-radius: 5px;
  }

  .blog-post h2 {
    margin: 0;
    font-size: 1.5rem;
  }

  .blog-post p {
    font-size: 0.9rem;
    color: #666;
  }
</style>
