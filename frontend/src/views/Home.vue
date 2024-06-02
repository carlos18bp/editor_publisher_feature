<template>
  <div class="flex space-x-24 m-4">
    <div class="w-1/2">
      <BlogEditor :action="action" />
    </div>
    <div class="w-1/3">
      <div v-show="!store.blogFocus">
        <BlogList @select-blog="showBlog" @edit-blog="editBlog" />
      </div>
      <div v-if="store.blogFocus">
        <Blog @back-to-list="showBlogList" @edit-blog="editBlog" />
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref } from 'vue'
  import BlogEditor from '@/components/BlogEditor.vue'
  import BlogList from '@/components/BlogList.vue'
  import Blog from '@/components/Blog.vue'
  import { useBlogStore } from '@/store/blog'

  // Initialize the blog store
  const store = useBlogStore()

  // Ref to manage the current action (create or update)
  const action = ref('create')

  /**
   * Sets the action to 'update' when a blog is selected.
   */
  const showBlog = () => {
    action.value = 'update'
  }

  /**
   * Sets the store to editing mode and updates the action to 'update'.
   */
  const editBlog = () => {
    store.isEditing = true
    action.value = 'update'
  }

  /**
   * Resets the blog focus and sets the action to 'create'.
   */
  const showBlogList = () => {
    store.blogFocus = null
    action.value = 'create'
  }
</script>

<style scoped>
</style>
