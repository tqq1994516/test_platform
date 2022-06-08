import { BasicColumn } from '/@/components/Table/src/types/table';

export function getBasicColumns(): BasicColumn[] {
  return [
    {
      title: 'ID',
      dataIndex: 'id',
      fixed: 'left',
      width: 200,
      sorter: true,
    },
    {
      title: '项目名称',
      dataIndex: 'name',
      width: 150,
      sorter: true,
    },
    {
      title: '项目描述',
      dataIndex: 'description',
    },
    {
      title: '管理员',
      dataIndex: 'masters',
      width: 150,
    },
    {
      title: '项目成员',
      dataIndex: 'members',
      width: 150,
    },
    {
      title: '创建者',
      dataIndex: 'owner',
      width: 50,
      defaultHidden: true,
    },
    {
      title: '创建时间',
      dataIndex: 'c_time',
      width: 150,
      defaultHidden: true,
    },
    {
      title: '最后更新时间',
      dataIndex: 'u_time',
      width: 150,
      defaultHidden: true,
    },
  ];
}
