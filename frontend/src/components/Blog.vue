<template>
  <div class="blog space-y-4">
    <h1><span class="font-bold">Title: </span>{{ blog.title }}</h1>
    <h2><span class="font-bold">Image description: </span></h2>
    <img :src="blog.image_header" alt="Blog image description">
    <h2><span class="font-bold">Content editor: </span></h2>
    <div v-html="blog.content"></div>
    <p>Published on: {{ formatDate(blog.created_at) }}</p>
    <button
      @click="$emit('back-to-list')"
      type="button"
      class="text-white bg-gradient-to-r from-cyan-400 via-green-500 to-green-600 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-green-300 shadow-lg shadow-green-500/50 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2">
      Create new Blog
    </button>
    <button
      v-if="!store.isEditing"
      @click="$emit('edit-blog')"
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
    <button
      @click="$emit('back-to-list')"
      type="button" 
      class="text-white bg-gradient-to-r from-pink-400 via-pink-500 to-pink-600 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-pink-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2">
      Back to Blog List
    </button>
  </div>
</template>

<script setup>
  import { onMounted, reactive, watch } from 'vue'
  import { useBlogStore } from '@/store/blog'

  // Initialize the blog store
  const store = useBlogStore()
  const blog = reactive({})

  // When the component is mounted, assign the focused blog from the store to the local reactive blog object
  onMounted(() => {
    Object.assign(blog, store.blogFocus)
  })

  // Watch for changes in the store's focused blog and update the local blog object accordingly
  watch(() => store.blogFocus, (newValue) => {
    Object.assign(blog, newValue)
  })

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
  ::v-deep ol {
    list-style-type: decimal;
  }

  .blog {
    padding: 2rem;
  }

  .blog h1 {
    margin-bottom: 1rem;
  }

  .blog p {
    font-size: 0.9rem;
    color: #666;
  }

  button {
    margin-top: 2rem;
    padding: 0.5rem 1rem;
    cursor: pointer;
  }
</style>
