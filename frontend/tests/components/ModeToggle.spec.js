import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import ModeToggle from '@/components/ModeToggle.vue'

describe('ModeToggle', () => {
  it('highlights active mode', () => {
    const wrapper = mount(ModeToggle, {
      props: { modelValue: 'learn' }
    })
    
    const buttons = wrapper.findAll('button')
    expect(buttons[0].classes()).toContain('active')
    expect(buttons[1].classes()).not.toContain('active')
  })

  it('emits mode change on click', async () => {
    const wrapper = mount(ModeToggle, {
      props: { modelValue: 'learn' }
    })
    
    await wrapper.findAll('button')[1].trigger('click')
    expect(wrapper.emitted('update:modelValue')[0]).toEqual(['recap'])
  })
})
