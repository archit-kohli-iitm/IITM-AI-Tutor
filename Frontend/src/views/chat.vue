<template>
  <div class="container-fluid bg-light vh-100 d-flex flex-column">

    <nav class="navbar navbar-light bg-warning px-3 w-100">
      <div class="mt-100">
        <img src="../assets/image.png" alt="IITM Logo" class="logo me-2" width="50" height="50" />
        <router-link to="/course" class="btn btn-light border-dark ms-2">Back</router-link>
      </div>
      <span class="navbar-brand mb-0 h1 text-dark">AI Tutor for {{ subjectName }}</span>
      <button class="btn btn-light border-dark" @click="logout">Logout</button>
    </nav>

    <div class="row flex-grow-1">
      <!-- Sidebar -->
      <div class="col-3 bg-white d-flex flex-column p-3">
        <div v-for="(chatList, subject) in chats" :key="subject" class="mb-4">
      
        <!-- Subject Button
        <div class="d-flex justify-content-center mb-1">
          <button class="btn w-75 text-center"
            :class="{ 'btn-danger text-white': selectedSubject === subject, 'btn-warning': selectedSubject !== subject }"
            @click="joinChat(subject)" style="background-color: #ffffff; color: black;">
            {{ subject }}
          </button>
        </div> -->

        <!-- New Chat Button -->
        <div class="d-flex justify-content-center mb-2">
          <button class="btn w-100 text-center border border-dark hover-icon"
            @click="createChat(subject)">
            New Chat
          </button>
        </div>
        <hr>
        <!-- Chat Titles under Subject -->
          <div v-for="chat in [...chatList].reverse()" :key="chat.chat_id" class="d-flex justify-content-center mt-1" style="padding-bottom: 10px;">
        
            <!-- Flex container for the button and the delete icon -->
            <div class="d-flex justify-content-between w-100">
            
              <!-- Container div for the button -->
              <button 
                class="btn w-100 text-center border border-dark"
                :class="selectedChatId === chat.chat_id ? 'btn-warning' : 'btn-light'"
                @click="selectChat(chat.chat_id)"
              >
                {{ chat.title }}
              </button>
              
              <!-- Delete Icon positioned separately -->
              <i class="fa fa-trash hover-icon" 
                @click.stop="deleteChat(chat.chat_id)"
                style="border: 1px solid black; color: black; border-radius: 20%; padding: 0px; font-size: 18px; cursor: pointer; display: flex; align-items: center; justify-content: center; height: 40px; width: 40px; margin-left: 10px;"
                >
              </i>

            </div>
        
          </div>
        </div>
      </div>
      
      <!-- Chat Area -->
      <div class="col-9 d-flex flex-column bg-light p-3 border">
        <div class="flex-grow-1 border rounded p-3 bg-white">
          <div v-for="(message, index) in messages" :key="index" class="mt-2">
            <p class="mb-1" v-html="renderMarkdown(message)"></p>
          </div>
        </div>

        <div class="d-flex mt-3">
          <input v-model="query" type="text" class="form-control border border-dark"
            placeholder="Enter your query here ........" @keyup.enter="askQuestion" />
          <button class="btn btn-warning ms-2" @click="askQuestion">Ask</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import "@/axios";

import { marked } from 'marked'; // for markdown

export default {
  data() {
    return {
      chats: { "PDSA": [] },
      subject: "PDSA",
      selectedSubject: null,
      selectedChatId: null,
      query: "",
      messages: [],
      user: null,
      token: null,
      baseUrl: axios.defaults.baseURL
    };
  },
  methods: {
    joinChat(subject) {
      this.selectedSubject = subject;
      this.selectedChatId = null;
      this.messages = [];
    },
    async createChat(subject) {
      let user = this.user;
      const token = this.token;
      try {
        const token = JSON.parse(user)["access_token"];
        let response = await axios.post("/chats/",{
            subject_id: 1, title: "Chat on "+new Date().toLocaleString('en-GB', { 
                day: '2-digit', 
                month: '2-digit', 
                year: '2-digit', 
                hour: '2-digit', 
                minute: '2-digit', 
                hour12: false 
              }).replace(/(\d+)\/(\d+)\/(\d+),\s(\d+):(\d+)/, '$2/$1/$3 at $4:$5')
          },{ headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );
        console.log(response.data)
        if (response.status === 201) {
          this.chats.PDSA.push(response.data.chat);
          this.messages = [];
          await this.selectChat(response.data.chat.chat_id);
          console.log("Chat Created:", response.data);
        }
      } catch (error) {
        console.error("Error creating chat:", error);
        alert("Failed to create chat. Please try again.");
      }
    },

    async askQuestion() {
      let user = this.user;
      const token = this.token;
      if (!this.selectedChatId) {
        try {
          const token = JSON.parse(user)["access_token"];
          let response = await axios.post("/chats/",{
              subject_id: 1, title: "Chat on "+new Date().toLocaleString('en-GB', { 
              day: '2-digit',
              month: '2-digit',
              year: '2-digit',
              hour: '2-digit',
              minute: '2-digit',
              hour12: false
            }).replace(/(\d+)\/(\d+)\/(\d+),\s(\d+):(\d+)/, '$2/$1/$3 at $4:$5')
            },{ headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
            }
          );
          console.log(response.data)
          if (response.status === 201) {
            this.chats.PDSA.push(response.data.chat);
            this.selectedChatId = response.data.chat.chat_id;
            console.log("Chat Created:", response.data);
          }
        } catch (error) {
          console.error("Error creating chat:", error);
          alert("Failed to create chat. Please try again.");
        }
      };
      if (!this.query.trim()) return;
      const userQuery = this.query;
      this.query = "";
      this.messages.push(`You: ${userQuery}`);
      try {
        const response = await fetch(`${this.baseUrl}/message/send`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            chat_id: this.selectedChatId,
            content: userQuery,
          }),
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let aiResponse = "AI Tutor: ";

        // Add initial empty response
        this.messages.push(aiResponse);

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          aiResponse += decoder.decode(value);
          // Update last message with accumulated response
          this.messages.splice(-1, 1, aiResponse);
        }
      } catch (error) {
        console.error("Error sending message:", error);
        this.messages.push("AI Tutor: Failed to send your message.");
      }
    },

    formatChatMessages(messages) {
      return messages.map(msg => {
        const prefix = msg.msg_type === 'user' ? 'You: ' : 'AI Tutor: ';
        return `${prefix}${msg.content.trim()}`;
      });
    },

    logout() {
      localStorage.clear();
      this.$router.push({ name: "HOME" })
    },
    async selectChat(chatId) {
      this.selectedChatId = chatId;
      const token = this.token;
      try {

        let response = await axios.get(`/chats/${this.selectedChatId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          }
        })
        console.log(response)
        if (response.status === 200) {
          this.messages = this.formatChatMessages(response.data.messages);
        }
        else {
          console.log(response.status)
        }
      }
      catch (error) {
        console.log(error);
      }
    },
    renderMarkdown(text) {
      if (text.startsWith("AI Tutor: ")) {
        const aiResponse = text.slice(10); // Remove "AI Tutor: " prefix
        return "AI Tutor: " + marked(aiResponse);
      }
      return marked(text); // Convert Markdown to HTML
    },
    async deleteChat(chat_id) {
        try {
          // Ensure the selected subject exists in the chats object
          if (!this.chats[this.subject]) {
            console.error(`No chats found for subject: ${this.subject}`);
            return;
          }
          const updatedSubjectChats = this.chats[this.subject].filter(chat => chat.chat_id !== chat_id);
          this.chats = {
            ...this.chats,
            [this.subject]: updatedSubjectChats,
          };
          if (chat_id == this.selectedChatId){
            this.messages = [];
            if (this.chats[this.subject].length <= 0){
              this.selectedChatId = null;
            }
            else{
              let newChatId = this.chats[this.subject][this.chats[this.subject].length - 1].chat_id;
              await this.selectChat(newChatId);
            }
          }
          // Call your API to delete the chat
          const response = await axios.delete(`/chats/${chat_id}`, {
            headers: {
              Authorization: `Bearer ${this.token}`, // Include token for authentication (if necessary)
            },
          });

          // If the chat is successfully deleted, remove it from the correct subject's chat list
          if (response.status === 200) {
            // this.chats[this.subject] = this.chats[this.subject].filter(chat => chat.chat_id !== chat_id);
            console.log(`Chat with ID ${chat_id} deleted successfully.`);
            // Refresh the page to reflect changes
            // window.location.reload();
          } else {
            console.error(`Failed to delete chat with ID ${chat_id}. Status: ${response.status}`);
            window.location.reload();
          }
        } catch (error) {
          console.error('Error deleting chat:', error);
          alert('There was an error deleting the chat.');
        }
      },
  },
  async mounted() {
    let user = localStorage.getItem("user-info");
    if (!user) {
      this.$router.push({ name: "Login" });
      return;
    }

    const token = JSON.parse(user)["access_token"];
    this.user = user;
    this.token = token;
    try {
      let response = await axios.get("/chats/", {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });
      console.log(response.data)
      if (response.data.length != 0) {
        this.chats = response.data.reduce((acc, chat) => {
          const subjectName = chat.subject.subject_name;
          if (!acc[subjectName]) acc[subjectName] = [];
          acc[subjectName].push(chat);
          return acc;
        }, {});
      }
      if (this.chats[this.subject].length <= 0){
        this.selectedChatId = null;
        this.messages = [];
      }
      else{
        let newChatId = this.chats[this.subject][this.chats[this.subject].length - 1].chat_id;
        await this.selectChat(newChatId);
      }
      console.log("Loaded chats", this.chats);

    } catch (error) {
      if (error.response?.status === 401) {
        alert("Session expired. Please log in again.");
        localStorage.clear();
        this.$router.push({ name: "Login" });
      }
      else {
        alert("Unknown Error");
        console.log(error)
      }
    }
  },
  computed: {
    subjectName() {
      return this.$route.query.subject || "Default Subject";
    }
  },
  watch: {
    "$route.query.subject"(newVal) {
      console.log("Subject changed to:", newVal);
    }
  }
};
</script>

<style scoped>
.container-fluid {
  height: 100vh;
}

.navbar {
  width: 100%;
}

.btn-light:hover,
.btn-primary:hover {
  background-color: lightblue;
}

.text-center {
  text-align: center;
}

.btn-danger {
  background-color: #a61c00 !important;
  border-color: #a61c00 !important;
}

.mb-4 {
  margin-bottom: 1.5rem !important;
}

.hover-icon:hover {
  background-color: lightblue; /* Light gray background on hover */
}
</style>