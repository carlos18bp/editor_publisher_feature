import { defineStore } from 'pinia'
import { create_request, get_request, delete_request, update_request } from '@/store/services/request_http'

export const useBlogStore = defineStore('blog', {
  state: () => ({
    blogFocus: null,
    isEditing: false,
    blogs: [],
  }),
  actions: {
    /**
     * Fetches all blogs from the server and updates the store.
     */
    async fetchBlogs() {
      try {
        const response = await get_request('blogs/')
        this.blogs = response
      } catch (error) {
        console.error('Failed to fetch blogs:', error)
      }
    },

    /**
     * Creates a new blog with the given form data.
     * @param {FormData} formData - The form data for the new blog.
     */
    async createBlog(formData) {
      try {
        const response = await create_request('blogs/', formData)
        this.blogFocus = response
      } catch (error) {
        console.error('Failed to create blog:', error)
      }
    },

    /**
     * Updates an existing blog with the given ID and form data.
     * @param {number} id - The ID of the blog to update.
     * @param {FormData} formData - The form data for updating the blog.
     * @returns {Object} - The updated blog object.
     */
    async updateBlog(id, formData) {
      try {
        const response = await update_request(`blogs/update/${id}/`, formData)
        this.blogFocus = response
        return response
      } catch (error) {
        console.error('Failed to update blog:', error)
      }
    },

    /**
     * Deletes a blog with the given ID.
     * @param {number} blog_id - The ID of the blog to delete.
     */
    async deleteBlog(blog_id) {
      try {
        await delete_request(`blogs/delete/${blog_id}/`)
        this.blogFocus = null
        this.blogs = this.blogs.filter(blog => blog.id !== blog_id)
      } catch (error) {
        console.error('Failed to delete blog:', error)
      }
    },
  },
})
