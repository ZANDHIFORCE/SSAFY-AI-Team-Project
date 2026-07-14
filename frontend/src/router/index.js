import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      name: "map-home",
      component: () => import("../views/MapHomeView.vue"),
    },
    {
      path: "/places/:placeId/posts",
      name: "board-list",
      component: () => import("../views/BoardListView.vue"),
      props: true,
    },
    {
      path: "/places/:placeId/posts/:postId",
      name: "post-detail",
      component: () => import("../views/PostDetailView.vue"),
      props: true,
    },
    {
      path: "/places/:placeId/write",
      name: "post-write",
      component: () => import("../views/PostWriteView.vue"),
      props: true,
    },
    {
      path: "/places/:placeId/posts/:postId/edit",
      name: "post-edit",
      component: () => import("../views/PostWriteView.vue"),
      props: true,
    },
  ],
});

export default router;
