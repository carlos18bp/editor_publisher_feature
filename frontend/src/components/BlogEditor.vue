<template>
  <div class="space-y-4">
    <h1 class="font-bold">Blog Post Editor</h1>
    <div class="relative z-0">
        <input
          v-model="blog.title"
          type="text" 
          id="floating_standard" 
          class="block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none focus:outline-none focus:ring-0 focus:border-blue-600 peer" 
          placeholder=" " />
        <label for="floating_standard" class="absolute text-sm text-gray-500 duration-300 transform -translate-y-6 scale-75 top-3 -z-10 origin-[0] peer-focus:start-0 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-6 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">
          Title
        </label>
    </div>
    <div class="relative z-0">
      <label 
        class="block mb-2 text-sm font-medium text-gray-900" 
        for="file_input">
        Upload Header Image
      </label>
      <input
        ref="fileInput"
        class="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50" 
        id="file_input" 
        type="file"
        @change="handleImageHeaderChange">
    </div>
    <div>
      <QuillEditor
        ref="quillEditor"
        v-model:content="blog.content"
        contentType="html"
        :toolbar="toolbarOptions"
        :modules="modules"
        placeholder="Here you can write the content of your blog and/or email"        
        @update:content="handleTextChange" />
    </div>
    <button
      @click="publishBlog"
      type="button" 
      class="text-white bg-gradient-to-r from-blue-500 via-blue-600 to-blue-700 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-blue-300 shadow-lg shadow-blue-500/50 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2">
      Publish Blog
    </button>
  </div>
</template>

<script setup>
  import { onMounted, reactive, ref, watch } from 'vue';
  import { QuillEditor } from '@vueup/vue-quill'
  import BlotFormatter from 'quill-blot-formatter';
  import QuillImageDropAndPaste from 'quill-image-drop-and-paste';
  import MagicUrl from 'quill-magic-url';
  import ImageCompress from 'quill-image-compress';
  import '@vueup/vue-quill/dist/vue-quill.snow.css'
  import { useBlogStore } from '@/store/blog'

  // Initialize the blog store and reactive blog object
  const store = useBlogStore()
  const props = defineProps({
    action: String,
  });
  const blog = reactive({
    id: '',
    title: '',
    image_header: '',
    content: '',
    created_at: '',
    updated_at: ''
  })
  const quillEditor = ref(null);
  const fileInput = ref(null)
  const fileLoaded = ref(false)

  // Quill editor toolbar options
  const toolbarOptions = [
    ['bold', 'italic', 'underline', 'strike'],
    ['link', 'image', 'video'],
    [{ 'header': 1 }, { 'header': 2 }],
    [{ 'list': 'ordered'}, { 'list': 'bullet' }, { 'list': 'check' }],
    [{ 'indent': '-1'}, { 'indent': '+1' }],
    [{ 'size': ['small', false, 'large', 'huge'] }],
    [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
    [{ 'color': [] }, { 'background': [] }],
    [{ 'font': [] }],
    [{ 'align': [] }],
    ['clean'],
  ];

  // Quill editor modules
  const modules = [
    {
      name: 'blotFormatter',
      module: BlotFormatter,
    },
    {
      name: 'imageDropAndPaste',
      module: QuillImageDropAndPaste,
      options: {
        handler: function (dataUrl, type, data) {}
      }
    },
    {
      name: 'magicUrl',
      module: MagicUrl,
      options: {}
    },
    {
      name: 'imageCompress',
      module: ImageCompress,
      options: {
        quality: 0.9,
        maxWidth: 1000,
        maxHeight: 1000,
        imageType: 'image/jpeg',
      }
    },
  ];

  // Lifecycle hook to initialize the blog object
  onMounted(() => {
    if (store.blogFocus) Object.assign(blog, store.blogFocus)
  });

  // Watch for changes in the store's focused blog and reset editor if necessary
  watch(() => store.blogFocus, (newValue) => {
    if (!newValue) reStartEditor()
  });

  // Watch for changes in editing state and update blog object accordingly
  watch(() => store.isEditing, (newValue) => {
    if (newValue) {
      Object.assign(blog, store.blogFocus)
    }
  });

  /**
  * Publishes the blog by creating or updating it based on the action prop.
  */
  const publishBlog = async () => {
    if (blog.title.trim() === '') {
      alert('Title cannot be empty');
      return;
    }

    if (!fileLoaded.value && props.action === 'create') {
      alert('The image header cannot be empty');
      return;
    }

    if (blog.content === '') {
      alert('The editor content cannot be empty');
      return;
    }

    try {
      if (props.action === 'create') Object.assign(blog, await store.createBlog(setFormData()))
      if (props.action === 'update') Object.assign(blog, await store.updateBlog(blog.id, setFormData()))

      reStartEditor() 
      await store.fetchBlogs()

      alert('Blog published successfully');  
      console.log('Blog published')
    } catch (error) {
      console.error('Failed to publish blog:', error)
    }
  }

  /**
  * Sets the form data for the blog, including title, content, and image header.
  * @returns {FormData} - The form data for the blog.
  */
  const setFormData = () => {
    const formData = new FormData()
    formData.append('title', blog.title)
    formData.append('content', blog.content)

    const currentDate = new Date();
    const formattedDate = currentDate.toISOString(); // Format 'YYYY-MM-DDTHH:MM:SS.mmmZ'
    formData.append('updated_at', formattedDate);

    if (blog.image_header && fileLoaded.value) {
      formData.append('image_header', blog.image_header)
    }

    return formData;
  };

  /**
  * Handles changes in the Quill editor content.
  */
  const handleTextChange = () => {
    // Handle text change event
  };

  /**
  * Handles changes in the image header file input.
  * @param {Event} event - The file input change event.
  */
  const handleImageHeaderChange = (event) => {
    const file = event.target.files[0]
    if (file) {
      blog.image_header = file
      fileLoaded.value = true
    }
  }

  /**
  * Resets the editor and blog object to initial state.
  */
  const reStartEditor = () => {
    blog.id = ''
    blog.title = ''
    blog.image_header = ''
    blog.content = ''
    blog.created_at = ''
    blog.updated_at = ''
    fileInput.value.value = null

    quillEditor.value.setContents([])
    fileLoaded.value = false
    store.isEditing = false
  };
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
