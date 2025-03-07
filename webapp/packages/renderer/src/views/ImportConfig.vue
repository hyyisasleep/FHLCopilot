<template>
  <div class="flex flex-col h-full px-5 pt-10 relative">
    <a-button
      type="text"
      class="!absolute !left-9 !top-18 !hover:bg-transparent"
      :onclick="goBack"
    >
      <arrow-left-outlined class="text-4xl text-slate dark:text-gray-200 opacity-25" />
    </a-button>
    <section class="ml-20 mt-2">
      <AlasTitle />
      <span>{{ t('import.title') }}</span>
    </section>
    <div class="flex h-full">
      <a-steps
        :current="current"
        direction="vertical"
        class="mt-10 ml-64 w-32 alas-steps h-64"
      >
        <a-step>
          {{ t('import.step1') }}
          <template #icon> 1</template>
        </a-step>
        <a-step>
          {{ t('import.step2') }}
          <template #icon> 2</template>
        </a-step>
        <a-step>
          {{ t('import.step3') }}
          <template #icon> 3</template>
        </a-step>
      </a-steps>
      <div class="w-fit h-full relative overflow-hidden alas-step-con-box">
        <div
          class="w-full h-full transition-all duration-500 ease-in-out absolute top-0 left-0 flex flex-col justify-between"
          :style="transformStep1"
        >
          <div>
            <a-typography-title :heading="3">{{ stepTipsOptions[current] }}</a-typography-title>
            <a-upload
              draggable
              multiple
              :custom-request="customRequest as any"
              accept=".json,.yaml"
            >
              <template #upload-button>
                <div class="alas-upload">
                  <div>
                    <a-typography-title
                      :heading="4"
                      class="opacity-25"
                    >
                      {{ t('import.file.choose') }}
                    </a-typography-title>
                  </div>
                </div>
              </template>
              <template #upload-item></template>
            </a-upload>
          </div>
        </div>
        <div
          class="w-full h-full transition-all duration-500 ease-in-out absolute top-0 left-0 z-36 flex flex-col justify-between"
          :style="transformStep2"
        >
          <div>
            <a-typography-title
              class="px-2 box-border"
              :heading="3"
            >
              {{ stepTipsOptions[current] }}
            </a-typography-title>
            <a-typography-text
              class="px-2 box-border"
              ellipsis
            >
              {{ fileParentPath }}{{ t('import.filePathTips') }}
            </a-typography-text>
            <section class="flex justify-between w-full px-2 box-border alas-file-title">
              <a-typography-title :heading="6">{{ t('import.fileName') }}</a-typography-title>
              <a-typography-title :heading="6">{{ t('import.lastModify') }}</a-typography-title>
            </section>
            <a-list class="alas-file-list overflow-y-auto overscroll-contain max-h-96">
              <a-list-item
                v-for="fileItem in fileItems"
                :key="fileItem.uid"
              >
                <a-list-item-meta :title="fileItem.name"></a-list-item-meta>
                <template #actions>
                  <span>{{ fileItem.lastModifyTime }}</span>
                </template>
              </a-list-item>
            </a-list>
          </div>

          <a-space class="pt-10 pb-15 flex justify-end align-content-end">
            <a-button
              :onclick="onCancel"
              size="large"
            >
              {{ t('import.btnGoBack') }}
            </a-button>
            <a-button
              type="primary"
              :onclick="onOkSave"
              size="large"
              :loading="saveLoading"
            >
              {{ t('import.btnImport') }}
            </a-button>
          </a-space>
        </div>
        <div
          class="w-full h-full transition-all duration-500 ease-in-out absolute top-0 left-0 z-36 flex flex-col justify-between"
          :style="transformStep3"
        >
          <div>
            <a-typography-title
              class="px-2 box-border"
              :heading="3"
            >
              {{ stepTipsOptions[current] }}
            </a-typography-title>
            <a-typography-text class="px-2 box-border">
              {{ configDirPath }} {{ t('import.filePathTips') }}
            </a-typography-text>
            <section class="flex justify-between w-full px-2 box-border alas-file-title">
              <a-typography-title :heading="6">{{ t('import.fileName') }}</a-typography-title>
              <a-typography-title :heading="6">{{ t('import.lastModify') }}</a-typography-title>
            </section>
            <a-list class="alas-file-list overflow-y-auto overscroll-contain max-h-96">
              <a-list-item
                v-for="fileItem in configDirFiles"
                :key="fileItem.uid"
              >
                <a-list-item-meta :title="fileItem.name"></a-list-item-meta>
                <template #actions>
                  <span>{{ fileItem.lastModifyTime }}</span>
                </template>
              </a-list-item>
            </a-list>
          </div>
          <a-space class="pt-10 pb-15 flex justify-end align-content-end">
            <a-button
              :onclick="onReimport"
              size="large"
            >
              {{ t('import.btnReimport') }}
            </a-button>
            <a-button
              type="primary"
              :onclick="goBack"
              size="large"
            >
              {{ t('import.btnOk') }}
            </a-button>
          </a-space>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import {computed, ref} from 'vue';
import AlasTitle from '/@/components/AlasTitle.vue';
import {ArrowLeftOutlined} from '@ant-design/icons-vue';
import router from '/@/router';
import {useI18n} from '/@/hooks/useI18n';
import dayjs from 'dayjs';
import {useAppStore} from '/@/store/modules/app';
import {Modal} from '@arco-design/web-vue';
import type {RequestOption, UploadRequest} from '@arco-design/web-vue/es/upload/interfaces';
import {nanoid} from 'nanoid';

const {t} = useI18n();

const stepTipsOptions = ref({
  1: t('import.step1'),
  2: t('import.step2'),
  3: t('import.step3'),
});

const appStore = useAppStore();

const saveLoading = ref<boolean>(false);

const fileItems = ref<
  {file: File | undefined; uid: string; name: string; lastModifyTime: string}[]
>([]);

const configDirFiles = ref<{uid: string; name: string; path: string; lastModifyTime: string}[]>([]);
const configDirPath = ref('');

const current = ref(1);

const fileParentPath = computed(() => {
  let pathStr = '';
  fileItems.value.forEach(item => {
    const [path] = item?.file?.path.split('AzurLaneAutoScript') || ['unknown'];
    if (pathStr !== path) pathStr = path;
  });
  return pathStr;
});

const transformStep1 = computed(() => {
  if (current.value === 1) return {transform: 'translateY(0)'};
  return {transform: 'translateY(-100%)', opacity: 0};
});
const transformStep2 = computed(() => {
  if (current.value === 1) return {transform: 'translateY(100%)', opacity: 0};
  if (current.value === 2) return {transform: 'translateY(0)'};
  return {transform: 'translateY(-100%)', opacity: 0};
});
const transformStep3 = computed(() => {
  if (current.value === 3) return {transform: 'translateY(0)'};
  return {transform: 'translateY(100%)', opacity: 0};
});

const goBack = () => {
  router.back();
};

const customRequest = (option: RequestOption): UploadRequest | undefined => {
  const {fileItem} = option;
  current.value = 2;
  fileItems.value.push({
    file: fileItem.file,
    uid: fileItem.uid,
    name: fileItem?.file?.name || '',
    lastModifyTime: dayjs(fileItem?.file?.lastModified || new Date()).format('YYYY-MM-DD HH:mm:ss'),
  });
  return undefined;
};

const onOkSave = async () => {
  saveLoading.value = true;
  const paths = fileItems.value.map(item => item.file?.path || '');
  if (paths.includes('')) {
    throw new Error('Wrong file path, please try again');
  }
  await window.__electron_preload__copyFilesToDir(paths, appStore.getAlasPath + '/config', {
    filedCallback: e => {
      Modal.error({
        title: 'Error Notification',
        content: e.toString(),
      });
    },
  });
  const {configPath = '', files = []} = window.__electron_preload__getAlasConfigDirFiles();
  configDirPath.value = configPath;
  configDirFiles.value = files.map(item => ({
    uid: nanoid(),
    name: item.name || '--',
    path: item.path || '--',
    lastModifyTime: dayjs(item.lastModifyTime || 0).format('YYYY-MM-DD HH:mm:ss'),
  }));

  saveLoading.value = false;

  current.value = 3;
};

const onCancel = () => {
  current.value = 1;
  fileItems.value = [];
};

const onReimport = onCancel;
</script>

<style lang="less" scoped>
.alas-steps {
  :deep(.arco-steps-item) {
    overflow: visible;
    width: 100px;
  }

  :deep(.arco-steps-item-content) {
    width: 200px;
    text-align: right;
    transform: translateX(-250px);
  }
  :deep(.arco-steps-item-finish) {
    .arco-steps-item-node {
      .arco-steps-icon {
        background-color: rgb(var(--gray-3));
        color: rgb(var(--primary-9));
      }
    }
  }
  :deep(.arco-steps-item-process) {
    .arco-steps-item-node {
      .arco-steps-icon {
        background-color: rgb(var(--primary-9));
      }
    }
  }
  :deep(.arco-steps-item-wait) {
    .arco-steps-item-node {
      .arco-steps-icon {
        border: 2px solid rgb(var(--primary-9));
        color: rgb(var(--primary-9));
      }
    }
  }
}

.alas-step-con-box {
  width: calc(100vw - 32rem);
}

.alas-upload {
  border-radius: 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  width: calc(100vw - 32rem);
  height: calc(100vh - 22rem);
  max-width: 789px;
  max-height: 485px;
}
.alas-file-title {
  border-bottom: 2px solid var(--color-border-3);
}

.alas-file-list {
  :deep(.arco-list-wrapper) {
    border: none;
  }

  :deep(.arco-list-bordered) {
    border: none;
  }

  .arco-list-split .arco-list-header,
  .arco-list-split .arco-list-item:not(:last-child) {
    border: none;
  }

  .arco-list-medium .arco-list-content-wrapper .arco-list-content > .arco-list-item {
    padding: 0.25rem 0.5rem;
  }
}

body[arco-theme='light'] {
  .alas-upload {
    border: 2px solid var(--color-border-1);
  }

  .alas-steps {
    :deep(.arco-steps-item-wait) {
      .arco-steps-item-node {
        .arco-steps-icon {
          background: var(--color-bg-4);
        }
      }
    }
  }
}

body[arco-theme='dark'] {
  .alas-upload {
    border: 2px solid var(--color-border-3);
  }

  .alas-steps {
    :deep(.arco-steps-item-wait) {
      .arco-steps-item-node {
        .arco-steps-icon {
          background: var(--color-bg-4);
        }
      }
    }
  }
}
</style>
