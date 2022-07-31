import { Persistent, BasicKeys } from '/@/utils/cache/persistent';
import { CacheTypeEnum } from '/@/enums/cacheEnum';
import projectSetting from '/@/settings/projectSetting';
import { TOKEN_KEY } from '/@/enums/cacheEnum';
import { Ref } from 'vue';
import { useUsersStore, UserSimpleState } from '/@/store/modules/user';
import { getUser } from '/@/api/sys/user';

const { permissionCacheType } = projectSetting;
const isLocal = permissionCacheType === CacheTypeEnum.LOCAL;

export function getToken() {
  return getAuthCache(TOKEN_KEY);
}

export function getAuthCache<T>(key: BasicKeys) {
  const fn = isLocal ? Persistent.getLocal : Persistent.getSession;
  return fn(key) as T;
}

export function setAuthCache(key: BasicKeys, value) {
  const fn = isLocal ? Persistent.setLocal : Persistent.setSession;
  return fn(key, value, true);
}

export function clearAuthCache(immediate = true) {
  const fn = isLocal ? Persistent.clearLocal : Persistent.clearSession;
  return fn(immediate);
}

export async function checkUser(user_id: number | string, user_info: Ref<UserSimpleState>) {
  const usersStore = useUsersStore();
  if (!usersStore.users.value && typeof user_id === 'number') {
    const { id, username } = await getUser(user_id);
    user_info.value['id'] = id;
    user_info.value['username'] = username;
    usersStore.addUser(user_info);
  } else if (usersStore.users.value && typeof user_id === 'number') {
    for (const user of usersStore.users.value) {
      if (user.id === user_id) {
        user_info.value = user;
        break;
      }
    }
  }
}