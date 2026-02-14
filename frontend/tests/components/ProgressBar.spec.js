import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import ProgressBar from '@/components/ProgressBar.vue'

describe('ProgressBar', () => {
  it('calculates progress percentage correctly', () => {
    const wrapper = mount(ProgressBar, {
      props: { currentIndex: 2, total: 10 }
    })
    
    expect(wrapper.text()).toContain('Card 3 of 10')
    expect(wrapper.text()).toContain('7 remaining')
  })

  it('shows correct remaining count', () => {
    const wrapper = mount(ProgressBar, {
      props: { currentIndex: 0, total: 5 }
    })
    
    expect(wrapper.text()).toContain('Card 1 of 5')
    expect(wrapper.text()).toContain('4 remaining')
  })

  it('shows 100% progress bar when on last card', () => {
    const wrapper = mount(ProgressBar, {
      props: { currentIndex: 9, total: 10 }
    })
    
    const fill = wrapper.find('.progress-bar-fill')
    expect(fill.attributes('style')).toContain('width: 100%')
  })
})
